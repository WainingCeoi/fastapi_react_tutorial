# Step 2 — First API

> **Goal:** the backend serves real data (contacts) as validated JSON.

## The big idea: an API is a menu of URLs

An **API** is the full list of things the frontend can ask the backend for. Each item is a
**URL + an HTTP method**, and each returns or accepts **JSON**.

## HTTP methods are verbs — mapped to CRUD

| CRUD | Verb | Example |
|---|---|---|
| **C**reate | `POST` | `POST /contacts` |
| **R**ead | `GET` | `GET /contacts` |
| **U**pdate | `PUT` / `PATCH` | `PUT /contacts/1` |
| **D**elete | `DELETE` | `DELETE /contacts/1` |

**REST convention:** URLs name *things* (nouns); the verb is the HTTP method.
`/contacts` = the collection, `/contacts/1` = one item. Never `/getContacts`.

## What JSON really is

```
   Python (backend)         on the wire (HTTP)          JavaScript (browser)
   [{"id":1, ...}]  ──serialize──►  '[{"id":1,...}]'  ──parse──►  JS objects
    (live objects)                    (just TEXT)                  (live objects)
```

- JSON is **text** — a language-neutral format both Python and JavaScript translate to/from.
- `return`ing a Python dict → FastAPI **serializes** it to JSON text → browser **parses** it back into objects.
- Looks like a Python dict, but: **double-quoted keys only**, `true`/`false`/`null` (lowercase), and values limited to **string / number / boolean / null / array / object**.

## Pydantic: the data "blueprint"

```python
from pydantic import BaseModel

class Contact(BaseModel):
    id: int
    name: str
    email: str
```

- A Pydantic model declares the exact **shape** your data must take.
- FastAPI **reads your type hints** and uses the model to **validate and document** automatically:
  - **Output:** `def get_all_contacts() -> list[Contact]` validates what you return.
  - **Input:** `def get_contact(contact_id: int)` validates what comes in.

## Path parameters + the "get-or-404" pattern

```python
@app.get("/contacts/{contact_id}")
def get_contact(contact_id: int) -> Contact:
    for contact in contacts:
        if contact["id"] == contact_id:
            return contact
    raise HTTPException(status_code=404, detail="Contact not found")
```

- `{contact_id}` = a **variable slot** in the URL, passed to the function argument of the same name.
- `contact_id: int` validates **input** — `/contacts/abc` auto-returns `422`.
- Two shapes of read endpoint:
  - **Collection** (`GET /contacts`) → returns a **list**; empty `[]` is a normal answer.
  - **Single item** (`GET /contacts/{id}`) → returns **one object**, or **`404`** if absent (not an empty list).

## HTTP status codes

| Family | Meaning | Examples |
|---|---|---|
| **2xx** | ✅ Success | `200 OK` |
| **4xx** | ❌ *Client's* fault | `404 Not Found`, `422 Unprocessable` |
| **5xx** | 💥 *Server's* fault | `500 Internal Server Error` |

## Gotchas & takeaways

- Return a wrongly-shaped response (e.g. a contact missing `email`) → Pydantic raises a **`500`**, and the **real, detailed error is in the server terminal** — the browser only shows a generic "Internal Server Error."
- **A browser `500` → go read the server log.**
- Input errors (bad path param) → **`422`, returned *to the client*** as helpful JSON. Safe to show, because it's the client's mistake. (4xx = safe to reveal; 5xx = hidden, could leak internals.)
- "Get one" returns a **single object + 404**, not a filtered list.
- One function → one name (duplicate function names silently shadow each other).

---
**← [Step 1](step-1-setup-and-hello-world.md) · Next → [Step 3 — First React Page](step-3-first-react-page.md)**
