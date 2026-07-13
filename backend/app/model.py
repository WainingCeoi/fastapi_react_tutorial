from sqlmodel import Field, SQLModel


class Contact(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    phone: str | None = None


class ContactCreate(SQLModel):
    name: str = Field(min_length=1)  # reject the empty string (not whitespace) at the boundary
    email: str
    phone: str | None = None


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
    username: str = Field(min_length=3, max_length=50)
    # max_length matters too: hashing is deliberately slow, so an unbounded
    # password lets anyone burn server CPU with multi-megabyte input
    password: str = Field(min_length=8, max_length=128)


class UserPublic(SQLModel):
    id: int
    username: str
