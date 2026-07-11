from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.database import SessionDep
from app.model import Contact, Note, NoteCreate

router = APIRouter(tags=["notes"])


@router.post("/contacts/{contact_id}/notes")
def create_note(contact_id: int, note_data: NoteCreate, session: SessionDep) -> Note:
    contact = session.get(Contact, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    note = Note(text=note_data.text, contact_id=contact_id)
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


@router.get("/contacts/{contact_id}/notes")
def get_notes(contact_id: int, session: SessionDep) -> list[Note]:
    notes = session.exec(select(Note).where(Note.contact_id == contact_id)).all()
    return notes