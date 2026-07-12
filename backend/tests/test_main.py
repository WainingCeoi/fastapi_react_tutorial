import pytest
from app.database import get_session
from app.main import app
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool


@pytest.fixture(name="client")
def client_fixture():
    # a throwaway in-memory database, built fresh for each test
    engine = create_engine(
        "sqlite://",  # in-memory (no file)
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)  # make the tables in it

    def get_session_override():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = (
        get_session_override  # swap in the TEST machine
    )
    yield TestClient(app)
    app.dependency_overrides.clear()  # restore the real one


def test_create_and_read_contact(client):
    response = client.post(
        "/contacts", json={"name": "Ada", "email": "ada@example.com"}
    )
    assert response.status_code == 200
    created = response.json()
    assert created["name"] == "Ada"
    assert created["id"] is not None

    response = client.get("/contacts")
    assert [c["name"] for c in response.json()] == [
        "Ada"
    ]  # fresh DB → only what we made


def test_delete_contact_cascades_notes(client):
    contact = client.post("/contacts", json={"name": "Gus", "email": "g@x.com"}).json()
    cid = contact["id"]
    client.post(f"/contacts/{cid}/notes", json={"text": "owes money"})
    client.post(f"/contacts/{cid}/notes", json={"text": "due soon"})
    assert len(client.get(f"/contacts/{cid}/notes").json()) == 2

    assert client.delete(f"/contacts/{cid}").status_code == 200
    assert client.get(f"/contacts/{cid}/notes").json() == []  # the cascade, proven


def test_get_missing_contact_returns_404(client):
    response = client.get("/contacts/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Contact not found"


def test_note_on_missing_contact_returns_404(client):
    response = client.post("/contacts/999/notes", json={"text": "ghost note"})
    assert response.status_code == 404


def test_put_missing_contact_returns_404(client):
    response = client.put(
        "/contacts/999", json={"name": "ghost", "email": "ghost@example.com"}
    )
    assert response.status_code == 404


def test_delete_missing_contact_returns_404(client):
    response = client.delete("/contacts/999")
    assert response.status_code == 404


def test_create_note(client):
    cid = client.post("/contacts", json={"name": "Ada", "email": "a@x.com"}).json()[
        "id"
    ]
    response = client.post(f"/contacts/{cid}/notes", json={"text": "call her"})
    assert response.status_code == 200
    note = response.json()
    assert note["text"] == "call her"
    assert note["contact_id"] == cid
    assert note["id"] is not None

    assert [n["text"] for n in client.get(f"/contacts/{cid}/notes").json()] == [
        "call her"
    ]


def test_update_contact(client):
    cid = client.post("/contacts", json={"name": "Ada", "email": "a@x.com"}).json()[
        "id"
    ]
    response = client.put(
        f"/contacts/{cid}", json={"name": "Ada Lovelace", "email": "ada@x.com"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Ada Lovelace"

    assert client.get(f"/contacts/{cid}").json()["email"] == "ada@x.com"


def test_me_with_token(client):
    client.post("/users", json={"username": "alice", "password": "hunter2"})
    login = client.post("/token", data={"username": "alice", "password": "hunter2"})
    token = login.json()["access_token"]

    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "alice"


def test_login_wrong_password(client):
    client.post("/users", json={"username": "alice", "password": "hunter2"})
    response = client.post("/token", data={"username": "alice", "password": "nope"})
    assert response.status_code == 401


def test_me_without_token(client):
    response = client.get("/users/me")  # no header at all — no setup needed
    assert response.status_code == 401


def test_register_does_not_leak_hash(client):
    response = client.post("/users", json={"username": "alice", "password": "hunter2"})
    assert response.status_code == 200
    assert "hashed_password" not in response.json()
    assert "password" not in response.json()
