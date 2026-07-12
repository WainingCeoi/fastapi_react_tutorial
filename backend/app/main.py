from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from app.database import create_db_and_tables, engine
from app.model import Contact
from app.routers import contacts, notes, users

from app.config import settings

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contacts.router)
app.include_router(notes.router)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"message": "Hello, world"}


def seed_data():
    with Session(engine) as session:
        if session.exec(select(Contact)).first() is None:
            session.add(Contact(name="Walter White", email="walter.white@example.com"))
            session.add(
                Contact(name="Jesse Pinkman", email="jesse.pinkman@example.com")
            )
            session.add(Contact(name="Saul Goodman", email="saul.goodman@example.com"))
            session.commit()


create_db_and_tables()
seed_data()
