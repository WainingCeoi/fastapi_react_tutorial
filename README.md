# 🧭 FastAPI + React — Learning Journey

Building a **Contacts & Notes** app from scratch to genuinely understand modern web
development — backend-first, one concept at a time, code written by hand.

> **How to use this file:** tick a box every time you finish something. The goal is *many
> small wins*. When every box in a step is checked, you've earned the commit at the bottom
> of that step. 🎯

---

## 📍 You are here

**Step 5 of 6 ✅ done — The Real App**   →   next up: **Step 6 — Grown-up Backend**
`▰▰▰▰▰▱`  ·  full app: contacts + notes, list + detail, CRUD from the UI
📌 *Pivot: frontend concepts are in hand — from here the focus is backend depth (AI assists the UI).*

---

## 🗺️ The mental model (why there are two servers)

```
  YOUR LAPTOP  (everything here is "localhost" = this same machine)

   ┌───────────┐   1. "give me the page"     ┌──────────────────┐
   │           │ ──────────────────────────► │   Vite server    │
   │  Browser  │   2. HTML + CSS + JS        │  localhost:5173  │
   │  (Chrome) │ ◄────────────────────────── │    FRONTEND      │
   │           │                             └──────────────────┘
   │           │
   │           │   3. JS calls the API       ┌──────────────────┐
   │           │ ──────────────────────────► │ Uvicorn+FastAPI  │  ──►  🗄️ SQLite
   │           │   4. JSON                   │  localhost:8000  │  ◄──   database.db
   │           │ ◄────────────────────────── │    BACKEND       │
   └───────────┘                             └──────────────────┘
```

Frontend = the looks. Backend = the brains. **The database = the memory** (persists to disk).

---

## 🧱 Tech stack

| Layer | Tool | Why |
|---|---|---|
| Backend framework | **FastAPI** | Friendly, fast, free interactive docs |
| Web server | **Uvicorn** | Runs the FastAPI app on a port |
| Data models | **Pydantic v2** | Validation; ships with FastAPI |
| Database | **SQLModel + SQLite** | SQLite is just a file — zero setup |
| Python manager | **uv** | Deps + virtualenv |
| Frontend | **React + Vite** | Modern, fast dev server + JSX compiler |
| Language | **Plain JavaScript**, **plain CSS** | Kept minimal on purpose |
| Data fetching | **fetch()** | Manual on purpose — see the moving parts |

---

## 📂 Project structure

A **monorepo**: two independent, self-contained subprojects side by side.

```
fastapi_react_tutorial/       ← git repo (the monorepo root)
├── README.md  .gitignore
├── docs/                     ← per-step tutorial notes (the "why" + diagrams)
│
├── backend/                  ← self-contained PYTHON project  ← main focus
│   ├── pyproject.toml  uv.lock  .python-version  .venv/  .gitignore
│   ├── database.db           ← the SQLite database (gitignored)
│   └── app/
│       ├── __init__.py
│       └── main.py           ← FastAPI app, models, DB, endpoints
│
└── frontend/                 ← self-contained JS project (React + Vite)
    ├── package.json  node_modules/  .gitignore
    └── src/
        ├── App.jsx           ← the route table (<Routes>)
        ├── ContactList.jsx   ← list view
        └── ContactDetail.jsx ← detail view (one contact + its notes)
```

---

## 🚀 Run it

Two servers = two terminals, each *inside* its own subproject.

**Backend** — terminal 1:
```bash
cd backend
uv run uvicorn app.main:app --reload
```
→ http://127.0.0.1:8000  ·  auto-docs at http://127.0.0.1:8000/docs

**Frontend** — terminal 2:
```bash
cd frontend
npm run dev
```
→ http://localhost:5173

---

## 🎯 Roadmap

### Step 1 — Setup & Hello World  ·  *client–server model*  ✅
- [x] The two-process (client–server) model
- [x] FastAPI + Uvicorn hello-world; the standard `app/` package layout
- [x] React scaffolded with Vite
- [x] 💾 commit: *"Step 1: FastAPI + React hello world"*

### Step 2 — First API  ·  *routes, JSON & Pydantic*  ✅
- [x] Routes, HTTP methods, REST URLs; what JSON really is
- [x] `Contact` Pydantic model; FastAPI validates input **and** output
- [x] Status codes (200/404/422/500); path params; get-or-404
- [x] 💾 commit: *"Step 2: contacts API with Pydantic validation"*

### Step 3 — First React Page  ·  *UI = f(state)*  ✅
- [x] Components & JSX; `useState`, `useEffect`, `fetch`
- [x] The three fetch states (loading / error / success)
- [x] **CORS** (browser-enforced) fixed with `CORSMiddleware`
- [x] 💾 commit: *"Step 3: React page fetching and rendering contacts"*

### Step 4 — A Database  ·  *persistence & CRUD*  ✅
- [x] SQLite (a file); **SQLModel** = model + table; `engine` + `Session`
- [x] Full CRUD (`POST`/`GET`/`PUT`/`DELETE`); DB-assigned ids
- [x] Data **persists across restarts**
- [x] 💾 commit: *"Step 4: SQLite database with full CRUD via SQLModel"*

### Step 5 — The Real App  ·  *relationships & UI*  ✅
- [x] Backend: **Notes**, one-to-many with Contacts (foreign key + nested routes)
- [x] Frontend: list view, detail view, and note forms
- [x] Controlled inputs; create & delete from the UI; `useEffect` dependencies
- [x] Client-side routing — hand-built the **React Router** migration (real URLs, survives refresh)
- [x] Post-review fixes: cascade-delete a contact's notes; not-found handling on direct URLs
- [x] 💾 commit: *"Step 5: notes relationship + interactive UI"*

### Step 6 — Grown-up Backend  ·  *the backend deep-dive* 🎯
- [ ] Dependency injection: a shared DB session via `Depends` (`get_session`)
- [ ] Split `main.py` into **routers / modules** (contacts, notes) + a clean package layout
- [ ] Config & settings (env vars via `pydantic-settings`)
- [ ] Automated **tests** with `pytest` + FastAPI `TestClient`
- [ ] **Auth** basics: password hashing, JWT tokens, protecting routes
- [ ] **Database migrations** with Alembic (evolving the schema safely)
- [ ] Concept: the strangler-fig pattern (migrating a legacy app onto this stack)
- [ ] 💾 commit(s)

---

## 🧠 Concepts unlocked

**Backend (your home turf):**
- [x] Client–server model; HTTP; `localhost` & ports; Uvicorn runs FastAPI
- [x] Standard project layout; commit source not artifacts
- [x] HTTP methods & CRUD; REST URLs; status codes (2xx/4xx/5xx)
- [x] JSON as text (serialize/parse); Pydantic validation from type hints
- [x] Path params; get-or-404 (`HTTPException`); request bodies vs path/query params
- [x] SQLite; SQLModel (model + table); `engine` vs `Session`; `add`/`commit`/`refresh`
- [x] Querying: `select` / `.where` / `session.get`; DB-assigned ids
- [x] **One-to-many relationships** (foreign keys + nested routes)
- [x] CORS & middleware (browser-enforced)

**Frontend (concepts in hand — enough to direct an AI):**
- [x] SPA vs. traditional multi-page site
- [x] Components & JSX; `useState` & "UI = f(state)"; `useEffect` + dependencies
- [x] `fetch` (GET/POST/DELETE); loading/error/success; immutable state updates
- [x] Controlled form inputs
- [x] **React Router** — `BrowserRouter` / `Routes` / `Route` / `Link` / `useParams` (URL-driven views)

**Coming up (Step 6 — backend):**
- [ ] Dependency injection (`Depends`); routers; config; testing
- [ ] Auth & JWT tokens; Alembic migrations

---

## 📓 Log

Jot a line here whenever something clicks or bites — future-you will thank you.

- **Step 1:** Standard layout — `backend/` and `frontend/` self-contained; run backend from
  inside `backend/` with `uvicorn app.main:app --reload`.
- **Step 2:** The API — `Contact` Pydantic model, get-or-404. A browser `500` → read the
  server terminal for the real error.
- **Step 3:** Frontend fetches & renders; hit and fixed **CORS** — it's *browser*-enforced
  (server said `200`, browser blocked the read).
- **Step 4:** Gave the app a memory — SQLModel table + SQLite + full CRUD. A contact added
  via the API **survived a restart**. The DB assigns ids; `refresh` reloads them after commit.
- **Step 5:** Real app — one-to-many **Notes** (foreign key), an interactive UI (list, detail,
  forms), and a hand-built **React Router** migration (URL-driven views that survive a refresh).
  A multi-agent adversarial review then caught two real edges: notes were orphaned on contact
  delete (added a cascade), and a direct URL to a missing contact rendered blank (added not-found
  handling). Pivoting to **backend depth** next; AI assists the UI from here.
