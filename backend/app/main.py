from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, SQLModel, create_engine, Session, select

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)


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


engine = create_engine("sqlite:///database.db", echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def seed_data():
    with Session(engine) as session:
        if session.exec(select(Contact)).first() is None:
            session.add(Contact(name="Walter White", email="walter.white@example.com"))
            session.add(Contact(name="Jesse Pinkman", email="jesse.pinkman@example.com"))
            session.add(Contact(name="Saul Goodman", email="saul.goodman@example.com"))
            session.commit()

create_db_and_tables()
seed_data()


@app.post("/contacts")
def create_contact(contact_data: ContactCreate) -> Contact:
    with Session(engine) as session:
        contact = Contact(name=contact_data.name, email=contact_data.email)
        session.add(contact)
        session.commit()
        session.refresh(contact)
        return contact


@app.get("/")
def read_root():
    return {"message": "Hello, world"}


@app.get("/contacts")
def get_all_contacts() -> list[Contact]:
    with Session(engine) as session:
        return session.exec(select(Contact)).all()


@app.get("/contacts/{contact_id}")
def get_contact(contact_id: int) -> Contact:
    with Session(engine) as session:
        contact = session.get(Contact, contact_id)
        if contact is None:
            raise HTTPException(status_code=404, detail="Contact not found")
        return contact


@app.put("/contacts/{contact_id}")
def update_contact(contact_id: int, contact_data: ContactCreate) -> Contact:
    with Session(engine) as session:
        contact = session.get(Contact, contact_id)
        if contact is None:
            raise HTTPException(status_code=404, detail="Contact not found")
        contact.name = contact_data.name
        contact.email = contact_data.email
        session.commit()
        session.refresh(contact)
        return contact


@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):
    with Session(engine) as session:
        contact = session.get(Contact, contact_id)
        if contact is None:
            raise HTTPException(status_code=404, detail="Contact not found")
        # Delete this contact's notes first, or they'd be orphaned: SQLite doesn't
        # enforce the foreign key, so they'd linger pointing at a contact that's gone.
        notes = session.exec(select(Note).where(Note.contact_id == contact_id)).all()
        for note in notes:
            session.delete(note)
        session.delete(contact)
        session.commit()
        return {"ok": True}


@app.post("/contacts/{contact_id}/notes")
def create_note(contact_id: int, note_data: NoteCreate) -> Note:
    with Session(engine) as session:
        contact = session.get(Contact, contact_id)
        if contact is None:                                  # can't note a ghost
            raise HTTPException(status_code=404, detail="Contact not found")
        note = Note(text=note_data.text, contact_id=contact_id)
        session.add(note)
        session.commit()
        session.refresh(note)
        return note
    

@app.get("/contacts/{contact_id}/notes")
def get_notes(contact_id: int) -> list[Note]:
    with Session(engine) as session:
        notes = session.exec(
            select(Note).where(Note.contact_id == contact_id)   # ← filter by the link
        ).all()
        return notes
