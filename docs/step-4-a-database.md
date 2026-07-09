# Step 4 — A Database

> **Goal:** give the app a *memory* — store contacts in a database so they survive restarts,
> with full Create / Read / Update / Delete.

## The big idea: from memory to disk

```
  BEFORE (in memory)              NOW (on disk)
  contacts = [ {...}, {...} ]     backend/database.db  ← a real file
  a Python list                   ┌────────────────────────┐
       │                          │     Contact Table      │
   gone on restart                │  id │ name   │ email   │
                                  │  1  │ ...    │ ...     │
                                  └────────────────────────┘
                                  survives restart ✅
```

- A **database** stores data **persistently** (on disk) and lets you **query** it.
- SQL databases store data in **tables** — rows are records, columns are fields.
- **SQLite** is the simplest kind: the whole database is **one file** (`database.db`), no
  separate server to install or run. Ideal for learning and small apps.

## SQLModel: one class, two jobs

```
   class Contact(SQLModel, table=True):
                    │            │
                    │            └─ table=True → it's also a DATABASE TABLE
                    └─ SQLModel → it's also a PYDANTIC MODEL (validation + JSON)
```

Your `Contact` is *both* the validation model *and* the table definition — no duplication.

```python
class Contact(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)   # the DB assigns the id
    name: str
    email: str
```

- `primary_key=True` — `id` uniquely identifies each row.
- `int | None` defaulting to `None` — **you don't set the id; the database generates it** on insert. (That's why real ids start at 1.)

## Engine + Session

```
  engine  ── the long-lived connection to database.db  (the "phone line")
     │
     └── Session ── ONE conversation / transaction  (a "phone call")
                    open → add / query → commit → close
```

```python
engine = create_engine("sqlite:///database.db", echo=True)   # echo=True → prints the SQL

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)   # CREATE TABLE for every table=True model
```

- The **engine** knows how to talk to the DB. You don't query it directly.
- A **`Session`** is a single unit of work. `with Session(engine) as session:` opens it and auto-closes.
- `echo=True` prints every SQL statement to the terminal — a window into the "magic."

## The CRUD map → endpoints

| CRUD | Verb + route | Session call |
|---|---|---|
| **C**reate | `POST /contacts` | `session.add(obj)` → `commit` → `refresh` |
| **R**ead all | `GET /contacts` | `session.exec(select(Contact)).all()` |
| **R**ead one | `GET /contacts/{id}` | `session.get(Contact, id)` |
| **U**pdate | `PUT /contacts/{id}` | fetch → change fields → `commit` |
| **D**elete | `DELETE /contacts/{id}` | `session.delete(obj)` → `commit` |

### Create (and where the request body comes from)

```python
class ContactCreate(SQLModel):   # input model — NO table=True, NO id
    name: str
    email: str

@app.post("/contacts")
def create_contact(contact_data: ContactCreate) -> Contact:
    with Session(engine) as session:
        contact = Contact(name=contact_data.name, email=contact_data.email)
        session.add(contact)       # stage
        session.commit()           # write (INSERT happens here)
        session.refresh(contact)   # reload so contact.id (DB-assigned) is filled in
        return contact
```

- **Where params come from:** a **simple-typed** param (`id: int`) = path/query; a
  **model-typed** param (`contact_data: ContactCreate`) = the **request body** (JSON).
- **Input model ≠ table model:** the client sends `name`/`email` but not `id` (the DB
  assigns it), so `ContactCreate` omits `id`. Input and table shapes often differ.

### Update & Delete

```python
@app.put("/contacts/{contact_id}")
def update_contact(contact_id: int, contact_data: ContactCreate) -> Contact:
    with Session(engine) as session:
        contact = session.get(Contact, contact_id)
        if contact is None:
            raise HTTPException(status_code=404, detail="Contact not found")
        contact.name = contact_data.name     # the object is TRACKED by the session…
        contact.email = contact_data.email
        session.commit()                      # …commit → UPDATE (no explicit "save")
        session.refresh(contact)
        return contact

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):
    with Session(engine) as session:
        contact = session.get(Contact, contact_id)
        if contact is None:
            raise HTTPException(status_code=404, detail="Contact not found")
        session.delete(contact)
        session.commit()
        return {"ok": True}
```

- `PUT` takes **both** a path param (which contact) **and** a body (the new data).
- **Unit of work:** an object fetched via `session.get` is *tracked* — change its fields
  and `commit()`, and SQLAlchemy figures out the `UPDATE` for you.

## Gotchas & takeaways

- **The database assigns ids** — model `id` as `int | None` with `default=None`.
- **`session.refresh(obj)` after `commit`** — `commit` "expires" the object; refresh reloads
  it so the new id (and current values) are populated before you return it.
- **SQLite creates the file, not the folder** — a parent directory must already exist.
- **Name resolution is at call time:** an endpoint function can reference `engine` even if
  `engine` is defined lower in the file — Python looks it up when the function *runs*, not
  when it's defined. (Still, order the file logically: setup first, endpoints last.)
- **Persistence proof:** add a contact via `/docs`, restart the server — it's still there,
  because it lives in `database.db`, not in memory.
- `echo=True` shows the real `CREATE TABLE` / `SELECT` / `INSERT` / `UPDATE` / `DELETE` SQL.
- Gitignore the DB file (`*.db`) — it's data/artifact, like `.venv`.

---
**← [Step 3](step-3-first-react-page.md) · Next → Step 5 (coming): The Real App**
