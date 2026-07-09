from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)

class Contact(BaseModel):
    id: int
    name: str
    email: str

contacts = [
    {"id": 1, "name": "Walter White", "email": "walter.white@example.com"},
    {"id": 2, "name": "Jesse Pinkman", "email": "jesse.pinkman@example.com"},
    {"id": 3, "name": "Saul Goodman", "email": "saul.goodman@example.com"},
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
