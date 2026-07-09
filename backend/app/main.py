from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Contact(BaseModel):
    id: int
    name: str
    email: str

contacts = [
    {"id": 1, "name": "John Doe", "email": "john.doe@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane.smith@example.com"}
]

@app.get("/")
def read_root():
    return {"message": "Hello, world"}

@app.get("/contacts")
def get_all_contacts() -> list[Contact]:
    return contacts

@app.get("/contacts/{contact_id}")
def get_contact(contact_id: int) -> Contact:
    for contact in contacts:
        if contact["id"] == contact_id:
            return contact
    raise HTTPException(status_code=404, detail="Contact not found")
