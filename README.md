# 🧭 FastAPI + React — Learning Journey

Building a **Contacts & Notes** app from scratch to genuinely understand modern web
development — backend-first, one concept at a time, code written by hand.

> **How to use this file:** tick a box every time you finish something. The goal is *many
> small wins*. When every box in a step is checked, you've earned the commit at the bottom
> of that step. 🎯

---

## 📍 You are here

**Step 7 of 7 ✅ done — Config, Auth & Migrations**   ·   🎉 the guided build is complete
`▰▰▰▰▰▰▰`  ·  secrets in the environment, JWT auth, and Alembic schema migrations
📌 *Backend is now production-shaped. Steps 7 & 8 merged into one "make it production-ready" arc.*

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
| Config | **pydantic-settings** | Secrets & settings from env / `.env`, validated |
| Auth — hashing | **pwdlib + Argon2** | Salted, one-way password hashing |
| Auth — tokens | **PyJWT** | Signed JWT access tokens (OAuth2 password flow) |
| Migrations | **Alembic** | Versioned, reversible schema changes |
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
│   ├── .env.example          ← settings template (committed — copy to .env)
│   ├── .env                  ← secrets & settings (gitignored!)
│   ├── database.db           ← the SQLite database (gitignored)
│   ├── alembic.ini           ← Alembic config
│   ├── alembic/              ← schema migrations
│   │   ├── env.py            ← wired to settings + SQLModel.metadata
│   │   └── versions/         ← one file per schema change (the history)
│   ├── tests/
│   │   └── test_main.py      ← pytest suite (TestClient + in-memory DB)
│   └── app/
│       ├── __init__.py
│       ├── main.py           ← wiring: middleware, include_router, startup
│       ├── config.py         ← Settings (pydantic-settings) ← reads .env
│       ├── model.py          ← SQLModel models (Contact, Note, User)
│       ├── database.py       ← engine, session (get_session / SessionDep)
│       ├── security.py       ← hashing, JWT, get_current_user
│       └── routers/          ← endpoints by resource (APIRouter)
│           ├── contacts.py
│           ├── notes.py
│           └── users.py      ← register, login (/token), /users/me
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
uv run alembic upgrade head          # create/upgrade the DB schema (first run + after model changes)
uv run uvicorn app.main:app --reload
```
→ http://127.0.0.1:8000  ·  auto-docs at http://127.0.0.1:8000/docs

> First run: `cp .env.example .env`, then fill in `SECRET_KEY` (generate one with
> `openssl rand -hex 32`). The app **fails fast** if a required value is missing.
> Coming from a pre-Alembic checkout? Your old `database.db` predates the migration
> history — simplest is to delete it and re-run (it only ever held seed data).

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
> Tests import the app, so a **valid** `.env` must exist first — do the first-run setup
> above (`SECRET_KEY` filled in; an empty one fails validation at import). But the tests
> themselves run entirely on a throwaway in-memory DB: no migrations, and `database.db`
> is never touched.

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

### Step 7 — Config, Auth & Migrations  ·  *making it production-ready*  ✅
- [x] Config/settings: DB URL, CORS origin & **`SECRET_KEY`** in env vars via `pydantic-settings`
- [x] Password **hashing** (salted, never plaintext) — **`pwdlib` + Argon2**
- [x] **JWT** login (`OAuth2` password flow via **PyJWT**): issue on `/token`, verify per request
- [x] Protect routes with an auth dependency — `get_current_user` / `CurrentUserDep`
- [x] The three-model split (`UserCreate` / `User` / `UserPublic`) so the hash never leaks
- [x] **Alembic** migrations — evolved the schema (added `Contact.phone`) with **zero data loss**
- [x] Concept: the **strangler-fig** pattern — evolve a legacy system incrementally, not big-bang
- [x] 💾 commit: *"Step 7 (config + auth): pydantic-settings, password hashing, JWT login"* (migrations to follow)

> **Steps 7 & 8 were merged** into this single "make it production-ready" arc.

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
- [x] **Config & secrets** — `pydantic-settings`, `.env`, fail-fast on missing required values
- [x] **Authentication** — salted hashing (Argon2), JWT (signed not encrypted), OAuth2 login, `get_current_user`
- [x] **Migrations** — Alembic autogenerate → review → `upgrade`; versioned, reversible schema history
- [x] **Strangler-fig** — evolving a real system incrementally behind a facade

**Frontend (concepts in hand — enough to direct an AI):**
- [x] SPA vs. traditional multi-page site
- [x] Components & JSX; `useState` & "UI = f(state)"; `useEffect` + dependencies
- [x] `fetch` (GET/POST/DELETE); loading/error/success; immutable state updates
- [x] Controlled form inputs
- [x] **React Router** — `BrowserRouter` / `Routes` / `Route` / `Link` / `useParams` (URL-driven views)

**🎉 The guided build is complete** — every planned concept is checked off. Natural next
extensions, whenever you want them: wire `phone` into the API, protect the contacts routes behind
`CurrentUserDep`, add refresh tokens, or point the backend at PostgreSQL.

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
- **Step 7:** Made it production-shaped — **config** (`pydantic-settings`; secrets in a gitignored
  `.env`; fail-fast when a required value is missing), **auth** (Argon2 password hashing, the
  three-model split so the hash never leaks, an OAuth2 `/token` login issuing **PyJWT** tokens, and
  `get_current_user` — protecting a route became *one dependency*, the DI payoff), and **Alembic
  migrations** (retired `create_all`; autogenerated an `add_column` that grew `Contact.phone` with
  **zero data loss**). Closed with the **strangler-fig** mindset. Recurring lesson: verify tools
  against live sources over stale memory (`pwdlib`/`PyJWT`, not the older `passlib`/`python-jose`).
- **Post-step review:** a 46-agent adversarial review confirmed 18 defects; all fixed. Headliners:
  module-level `seed_data()` ran at *import* (crashed fresh clones; let pytest silently seed the real
  `database.db`) → moved to a **lifespan handler**; `echo=True` was printing password hashes into
  server logs → now a `db_echo` setting (default off); `Contact.phone` was write-unreachable;
  `UserCreate` accepted empty/giant credentials → length constraints; SQLite FK enforcement turned on
  (`PRAGMA foreign_keys=ON`); the frontend's unchecked `fetch`es + stale-closure state bugs fixed
  (`response.ok` everywhere, functional updates, `AbortController`). Verification then caught a bonus:
  an **empty** `SECRET_KEY=` passed validation ("" is a `str`!) and only failed at login —
  `min_length=32` now fails it at boot. Tests: 12 → **15**.
