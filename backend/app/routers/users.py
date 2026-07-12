from typing import Annotated

from app.database import SessionDep
from app.model import User, UserCreate, UserPublic
from app.security import (
    CurrentUserDep,
    create_access_token,
    hash_password,
    verify_password,
)
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

router = APIRouter(tags=["users"])


@router.post("/users")
def create_user(user_data: UserCreate, session: SessionDep) -> UserPublic:
    existing_user = session.exec(
        select(User).where(User.username == user_data.username)
    ).first()
    if existing_user is not None:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = hash_password(user_data.password)
    user = User(username=user_data.username, hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/token")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
) -> dict:
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/users/me")
def read_current_user(current_user: CurrentUserDep) -> UserPublic:
    return current_user