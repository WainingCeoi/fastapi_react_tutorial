# Step 6 — Backend Architecture

> **Goal:** reshape a working-but-messy backend into production form — injected sessions, an
> automated test suite, and a modular package — *without changing any behavior*.

---

## Part A — Dependency Injection (`Depends`)

Every endpoint used to open its own session (`with Session(engine) as session:`), repeated
seven times and hard-wired to the global `engine`. **Dependency injection** flips that: an
endpoint *declares* what it needs, and FastAPI *provides* it.

```python
# database.py
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# an endpoint just asks for one:
def get_all_contacts(session: SessionDep) -> list[Contact]:
    return session.exec(select(Contact)).all()
```

**Mental model — a per-request vending machine.** For each request FastAPI "presses the
button" on `get_session`, which dispenses a **fresh** session; after the response it reclaims
and closes it (the code *after* `yield`).

```
  request → FastAPI runs get_session up to `yield` (opens a NEW session) → injects it
          → endpoint runs → response sent → resumes past `yield` (closes it)
  next request → the whole cycle again, with a brand-new session
```

- **Fresh per request** — nothing is shared or held between requests (same resource use as before).
- **Endpoints only** — `Depends` fires *only* inside FastAPI request handling. Startup code like
  `seed_data` is not an endpoint, so it opens its own `with Session(engine)`. (`seed_data(SessionDep)`
  fails — you'd be passing a *type*, not a session.)
- **The real payoff is testability** — see Part B.

---

## Part B — Automated tests (`pytest` + `TestClient`)

Tests are code that checks your code: write the assertions once, run `pytest` anytime.

- **`TestClient`** drives your real app *in-process* (`client.get("/contacts")`) — no server, no network.
- **`app.dependency_overrides[get_session] = ...`** swaps the vending machine for one that
  dispenses **in-memory test-DB** sessions, so tests never touch `database.db`. *(This is the clean
  version of monkeypatching the global engine — and it's exactly what DI bought you.)*

```python
@pytest.fixture(name="client")
def client_fixture():
    engine = create_engine("sqlite://",                       # in-memory
                           connect_args={"check_same_thread": False},
                           poolclass=StaticPool)               # one shared connection/DB
    SQLModel.metadata.create_all(engine)

    def get_session_override():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_session_override
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_delete_contact_cascades_notes(client):
    cid = client.post("/contacts", json={"name": "Gus", "email": "g@x.com"}).json()["id"]
    client.post(f"/contacts/{cid}/notes", json={"text": "owes money"})
    client.delete(f"/contacts/{cid}")
    assert client.get(f"/contacts/{cid}/notes").json() == []   # the cascade, proven
```

Habits that matter:
- **Arrange → Act → Assert** — set up data, do the thing, check the result.
- **Test the *unhappy* path** — the 404s. Bugs live in error handling, not the happy path.
- **Test behavior through the API** (status + JSON), never internals — so refactors don't break tests.
- **Isolation** — a fresh in-memory DB per test, so tests never interfere (you can assert exact results).

---

## Part C — Project structure (`APIRouter`)

One ~130-line `main.py` became a package where each file has *one job*:

```
app/
├── main.py        ← wiring only: middleware, include_router, startup
├── model.py       ← SQLModel models
├── database.py    ← engine, get_session, SessionDep, create_db_and_tables
└── routers/
    ├── contacts.py  ← APIRouter with the contact endpoints
    └── notes.py     ← APIRouter with the note endpoints
```

- **`APIRouter`** is a mini-collection of routes — `@router.get(...)` instead of `@app.get(...)`.
- **`app.include_router(contacts.router)`** plugs all its routes into the app — *same URLs*, tidier code.
- **Import order matters:** `create_all` builds tables for every model registered by the time it
  runs, and a model registers when its class is imported — so `main.py` imports the models
  (directly or via the routers) *before* calling `create_db_and_tables()`.

---

## Gotchas & takeaways

- **DI is endpoint-only.** `Depends` resolves during request handling; plain functions (seeding,
  scripts) open their own session.
- **A per-request session is fresh, not shared** — the wins are DRY + testability, not efficiency.
- **Tests make refactoring fearless.** This step moved code across five files, three times; the
  suite confirmed identical behavior every time. *That's why you write tests before refactoring.*
- **`main.py` should read like a table of contents** — wiring, not logic.
- **`TestClient` needs the real `httpx`** (versions `0.x`), *not* `httpx2` — declare dev deps precisely.

---
**← [Step 5](step-5-the-real-app.md) · Next → Step 7 (coming): Config & Auth**
