# 🧭 FastAPI + React — Learning Journey

Building a **Contacts & Notes** app from scratch to genuinely understand modern web
development — backend-first, one concept at a time, code written by hand.

> **How to use this file:** tick a box every time you finish something. The goal is *many
> small wins*. When every box in a step is checked, you've earned the commit at the bottom
> of that step. 🎯

---

## 📍 You are here

**Step 6 of 8 ✅ done — Backend Architecture**   →   next up: **Step 7 — Config & Auth**
`▰▰▰▰▰▰▱▱`  ·  injected sessions, a real test suite, and a modular package
📌 *Focus is backend depth (AI assists the UI). The old catch-all "Step 6" is now split into 6–8.*

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
| Testing | **pytest + TestClient** | In-process API tests, no server, throwaway DB |
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
│   ├── tests/
│   │   └── test_main.py      ← pytest suite (TestClient + in-memory DB)
│   └── app/
│       ├── __init__.py
│       ├── main.py           ← wiring: middleware, include_router, startup
│       ├── model.py          ← SQLModel models
│       ├── database.py       ← engine, session (get_session / SessionDep)
│       └── routers/          ← endpoints by resource (APIRouter)
│           ├── contacts.py
│           └── notes.py
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

**Tests** (backend):
```bash
cd backend
uv run pytest
```

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
- [x] Client-side routing — hand-built the **React Router** migration (real URLs, survives refresh)
- [x] Post-review fixes: cascade-delete a contact's notes; not-found handling on direct URLs
- [x] 💾 commit: *"Step 5: React Router migration + review fixes"*

### Step 6 — Backend Architecture  ·  *DI, testing, structure*  ✅
- [x] **Dependency injection** — a per-request DB session via `Depends` (`get_session` / `SessionDep`)
- [x] **Automated tests** — `pytest` + `TestClient`, overriding `get_session` onto an in-memory DB
- [x] Cover the **unhappy paths** (all four 404s) + the cascade-delete behavior
- [x] **Project structure** — split into `model.py`, `database.py`, and `routers/` (`APIRouter`)
- [x] `main.py` reduced to pure wiring (`include_router`)
- [x] 💾 commit: *"Step 6: dependency injection, tests, and router-based structure"*

### Step 7 — Config & Auth  ·  new idea: *settings & securing the API* 🎯
- [ ] Config/settings: move values (DB URL, secret key) to env vars via `pydantic-settings`
- [ ] Password **hashing** (never store plaintext) — `passlib` / `bcrypt`
- [ ] **JWT** tokens: issue on login, verify on requests
- [ ] Protect routes with an auth dependency (`Depends`)
- [ ] 💾 commit(s)

### Step 8 — Migrations & the Strangler-Fig  ·  *evolving & adopting* (stretch)
- [ ] **Alembic** migrations — change the schema without dropping data
- [ ] Concept: the **strangler-fig** pattern — migrating a legacy app onto this stack incrementally
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
- [x] **Dependency injection** (`Depends` / `SessionDep`) — endpoint-only, a fresh session per request
- [x] **Automated testing** — `pytest`, `TestClient`, `dependency_overrides`, fixtures, in-memory DB
- [x] **Project structure** — `APIRouter` + `include_router`; separation of concerns

**Frontend (concepts in hand — enough to direct an AI):**
- [x] SPA vs. traditional multi-page site
- [x] Components & JSX; `useState` & "UI = f(state)"; `useEffect` + dependencies
- [x] `fetch` (GET/POST/DELETE); loading/error/success; immutable state updates
- [x] Controlled form inputs
- [x] **React Router** — `BrowserRouter` / `Routes` / `Route` / `Link` / `useParams` (URL-driven views)

**Coming up (Steps 7–8 — backend):**
- [ ] Config/settings (`pydantic-settings`); password hashing; **JWT auth**
- [ ] Alembic migrations; the strangler-fig pattern

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
- **Step 5:** Real app — one-to-many **Notes** (foreign key), an interactive UI, and a hand-built
  **React Router** migration. A multi-agent review caught two edges (orphaned notes on delete →
  cascade; blank page on a missing direct URL → not-found handling). Pivoted to backend depth.
- **Step 6:** Reshaped the backend to production form — **dependency injection** (`get_session`
  as a per-request "vending machine"), a real **pytest + TestClient** suite (8 tests, incl. the
  404s and the cascade), and a modular **package** (`model` / `database` / `routers`) with
  `main.py` as pure wiring. The tests then blessed the refactor unchanged — the point of writing
  them first. (Supply-chain lesson: Starlette now wants **`httpx2`** — Pydantic's real successor to
  `httpx`, *not* a typosquat — which we confirmed against PyPI + `github.com/pydantic/httpx2` before
  trusting the deprecation warning.)
