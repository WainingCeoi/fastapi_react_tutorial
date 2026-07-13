from app.database import SessionDep
from app.model import Contact, ContactCreate, Note
from fastapi import APIRouter, HTTPException
from sqlmodel import select

router = APIRouter(tags=["contacts"])  # tags → groups these under "contacts" in /docs


@router.post("/contacts")
def create_contact(contact_data: ContactCreate, session: SessionDep) -> Contact:
    contact = Contact(
        name=contact_data.name, email=contact_data.email, phone=contact_data.phone
    )
    session.add(contact)
    session.commit()
    session.refresh(contact)
    return contact


@router.get("/contacts")
def get_all_contacts(session: SessionDep) -> list[Contact]:
    return session.exec(select(Contact)).all()


@router.get("/contacts/{contact_id}")
def get_contact(contact_id: int, session: SessionDep) -> Contact:
    contact = session.get(Contact, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/contacts/{contact_id}")
def update_contact(
    contact_id: int, contact_data: ContactCreate, session: SessionDep
) -> Contact:
    contact = session.get(Contact, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    contact.name = contact_data.name
    contact.email = contact_data.email
    contact.phone = contact_data.phone
    session.commit()
    session.refresh(contact)
    return contact


@router.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, session: SessionDep):
    contact = session.get(Contact, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    notes = session.exec(select(Note).where(Note.contact_id == contact_id)).all()
    for note in notes:
        session.delete(note)
    session.delete(contact)
    session.commit()
    return {"ok": True}
