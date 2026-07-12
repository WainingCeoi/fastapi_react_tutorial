from sqlmodel import Field, SQLModel


class Contact(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str


class ContactCreate(SQLModel):
    name: str
    email: str


class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str
    contact_id: int = Field(foreign_key="contact.id")


class NoteCreate(SQLModel):
    text: str


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str


class UserCreate(SQLModel):
    username: str
    password: str


class UserPublic(SQLModel):
    id: int
    username: str
