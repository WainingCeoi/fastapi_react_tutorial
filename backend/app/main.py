from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, SQLModel

from app.config import settings
from app.database import engine
from app.model import Contact
from app.routers import contacts, notes, users


def seed_data():
    with Session(engine) as session:
        if session.exec(select(Contact)).first() is None:
            session.add(Contact(name="Walter White", email="walter.white@example.com"))
            session.add(
                Contact(name="Jesse Pinkman", email="jesse.pinkman@example.com")
            )
            session.add(Contact(name="Saul Goodman", email="saul.goodman@example.com"))
            session.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: runs once when the SERVER starts (not when the module is imported)
    # — by now `alembic upgrade head` has built the schema
    SQLModel.metadata.create_all(engine)
    seed_data()
    yield  # the app serves requests while parked here
    # shutdown: anything after the yield would run when the server stops


app = FastAPI(lifespan=lifespan)
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
