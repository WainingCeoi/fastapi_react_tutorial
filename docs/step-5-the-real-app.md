# Step 5 — The Real App

> **Goal:** model a real *relationship* (a contact has many notes) and turn the read-only
> page into an interactive app (list → detail, with forms).

---

## Part A — Backend: the one-to-many relationship

The most important data-modeling idea in real apps: **a contact *has many* notes.** Flat SQL
tables can't nest a list inside a row, so the relational trick is to flip it — the **"many"
side holds a pointer back to the "one":**

```
   contact table                    note table
   ┌────┬──────────────┐            ┌────┬──────────────┬────────────┐
   │ id │ name         │            │ id │ text         │ contact_id │ ← foreign key
   ├────┼──────────────┤            ├────┼──────────────┼────────────┤
   │ 1  │ Walter White │◄───┐       │ 1  │ "Owes $"     │     1      │
   │ 2  │ Jesse Pinkman│    └───────│ 2  │ "Due soon"   │     1      │
   └────┴──────────────┘            └────┴──────────────┴────────────┘
        one contact ──has many──►  notes (each stores its contact_id)
```

```python
class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str
    contact_id: int = Field(foreign_key="contact.id")   # the link
```

- **Foreign key:** `contact_id` holds the id of the owning contact. That column *is* the relationship.
- **Nested routes** express ownership: `POST /contacts/{id}/notes`, `GET /contacts/{id}/notes`.
- **Fetch the "many"** with a `WHERE` on the foreign key:
  ```python
  session.exec(select(Note).where(Note.contact_id == contact_id)).all()
  ```

> Key flip to remember: the **"many" side holds the foreign key**, not the "one." (A contact
> doesn't "contain" notes; each note points to its contact.)

---

## Part B — Frontend: from displaying data to a real app

### Traditional website vs. Single-Page App (the core mental model)

```
TRADITIONAL (multi-page)              SINGLE-PAGE APP (React)
  server has one HTML page per URL      server sends ONE page + JS bundle, once
  click → GET new page → full reload     click → JS swaps elements, no reload
  🐢 screen blanks & reloads             ⚡ only changed elements repaint
```

- A **traditional site**: every URL is a separate HTML page from the server; navigating
  fetches a whole new page (the screen blanks and reloads).
- Your **React app (SPA)**: the server sends one near-empty `index.html` + a JavaScript
  bundle *once*. That JS **is** React; it paints the UI into the page and repaints only
  what changes. No full reloads — that's why it feels instant.

### Client-side routing (showing different "views")

An SPA has **one URL** but you want multiple views (a list *and* a detail). This project did it
**both ways** — first the simple version to learn the idea, then the real tool:

| Approach | How | Trade-off |
|---|---|---|
| **State (simple)** | a `selectedId` state + conditional render | no URL change → not bookmarkable / no Back button |
| **React Router** ✅ | a library that gives real URLs (`/contacts/:id`) | shareable URLs + Back button + survives refresh |

**React Router is just a route table — like FastAPI's, but it renders a component instead of
returning JSON:**

| | FastAPI (backend) | React Router (frontend) |
|---|---|---|
| Declare a route | `@app.get("/contacts/{id}")` | `<Route path="/contacts/:id" element={<ContactDetail/>}/>` |
| Read the URL param | `def get(id: int)` | `const { id } = useParams()` |
| Navigate | (the client) | `<Link to="/contacts/1">` (no reload) |

The four pieces: **`<BrowserRouter>`** (wraps the app, connects it to the URL bar) →
**`<Routes>`/`<Route>`** (the URL→component map) → **`<Link>`** (navigate without a reload) →
**`useParams()`** (read `:id`). The **payoff:** because `ContactDetail` rebuilds itself from the
URL's `id`, the detail page **survives a refresh** and is shareable — which the state version
couldn't do.

> "Changing the URL" and "reloading the page" are **different** — a router changes the URL bar
> *without* a server round-trip.

### Controlled forms & mutations from the UI

- **Controlled input:** `value={x}` + `onChange={(e) => setX(e.target.value)}` — React state
  is the single source of truth for the box. (`UI = f(state)`, for a text field.)
- **Submit:** `<form onSubmit={...}>` + `event.preventDefault()` (stop the default page reload).
- **Send data:** `fetch(url, { method, headers: {"Content-Type": "application/json"}, body: JSON.stringify(obj) })`.
- **Update state immutably** — build a *new* array, never mutate:
  - add → `setItems([...items, newItem])`
  - remove → `setItems(items.filter((i) => i.id !== id))`

### `useEffect` dependencies

```jsx
useEffect(() => { /* fetch */ }, [])            // run ONCE, after first render
useEffect(() => { /* fetch */ }, [selectedId])  // re-run whenever selectedId changes
```

The dependency array is the effect's **watch list**: empty = run once; `[selectedId]` =
re-run when it changes (so switching contacts re-fetches that contact's notes).

---

## Gotchas & takeaways

- **One-to-many:** the *many* side stores the foreign key.
- **SPA vs traditional:** a URL change is not a page reload; SPAs avoid full reloads.
- **Controlled inputs:** state is the source of truth for form fields.
- **Immutable state:** replace arrays (`[...]`, `.filter`), never mutate them.
- **Effect dependency array** decides *when* an effect re-runs.
- **Template literals need backticks** (`` `...${x}...` ``) — JS's f-string; quotes won't interpolate.
- **URL-addressable views must handle "not found":** once `/contacts/:id` is reachable by direct
  URL, someone *will* hit `/contacts/999` (typo, stale bookmark, deleted contact). Check
  `response.ok` and render a not-found state — otherwise the 404 body is stored as the "contact"
  and the page renders blank.
- **One-to-many cleanup:** deleting the "one" should delete its "many." SQLite doesn't cascade for
  you, so `delete_contact` must delete the contact's notes too — or they orphan (rows pointing at a
  contact that no longer exists).

---
**← [Step 4](step-4-a-database.md) · Next → Step 6 (coming): Grown-up Backend**
