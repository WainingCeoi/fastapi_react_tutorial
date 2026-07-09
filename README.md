# 🧭 FastAPI + React — Learning Journey

Building a **Contacts & Notes** app from scratch to genuinely understand modern web
development — backend-first, one concept at a time, code written by hand.

> **How to use this file:** tick a box every time you finish something. The goal is *many
> small wins*. When every box in a step is checked, you've earned the commit at the bottom
> of that step. 🎯

---

## 📍 You are here

**Step 2 of 6 ✅ done — First API**   →   next up: **Step 3 — First React Page**
`▰▰▱▱▱▱`  ·  backend now serves validated JSON · frontend is still the Vite starter

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
   │           │ ──────────────────────────► │ Uvicorn+FastAPI  │
   │           │   4. JSON: {"name": "Ada"}  │  localhost:8000  │
   │           │ ◄────────────────────────── │    BACKEND       │
   └───────────┘                             └──────────────────┘
```

Frontend = the looks. Backend = the brains & memory. They talk over **HTTP**.

---

## 🧱 Tech stack

| Layer | Tool | Why |
|---|---|---|
| Backend framework | **FastAPI** | Friendly, fast, free interactive docs |
| Web server | **Uvicorn** | Runs the FastAPI app on a port |
| Data models | **Pydantic v2** | Validation; ships with FastAPI |
| Database | **SQLModel + SQLite** | SQLite is just a file — zero setup (Step 4) |
| Python manager | **uv** | Deps + virtualenv |
| Frontend | **React + Vite** | Modern, fast dev server + JSX compiler |
| Language | **Plain JavaScript**, **plain CSS** | Add TypeScript / frameworks *later* |
| Data fetching | **fetch()** → TanStack Query later | Feel the manual pain first |

---

## 📂 Project structure

A **monorepo**: two independent, self-contained subprojects side by side.

```
fastapi_react_tutorial/       ← git repo (the monorepo root)
├── README.md                 ← this study tracker
├── .gitignore                ← OS/editor junk only
│
├── backend/                  ← self-contained PYTHON project
│   ├── pyproject.toml        ← backend deps & metadata
│   ├── uv.lock               ← exact pinned versions
│   ├── .python-version       ← pins Python 3.14
│   ├── .venv/                ← installed deps (gitignored, disposable)
│   ├── .gitignore            ← Python ignores
│   └── app/                  ← the application PACKAGE
│       ├── __init__.py       ← marks app/ as an importable package
│       └── main.py           ← the FastAPI app + endpoints
│
└── frontend/                 ← self-contained JS project
    ├── package.json          ← frontend deps & metadata
    ├── node_modules/         ← installed deps (gitignored, disposable)
    ├── .gitignore            ← Node ignores
    └── src/                  ← React components live here
```

> Each half owns its deps and its `.gitignore`, and each can be **run, tested, and
> deployed on its own**. That independence is the whole point of the split.

---

## 🚀 Run it

Two servers = two terminals, each sitting *inside* its own subproject.

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

> `app.main:app` = the **`app/`** package → its **`main.py`** module → the FastAPI
> object named **`app`** inside it. (Yes — "app" means two different things there!)

---

## 🎯 Roadmap

### Step 1 — Setup & Hello World  ·  *client–server model*  ✅
- [x] Confirm the stack & the build target
- [x] Understand the two-process (client–server) model
- [x] Backend: install FastAPI + Uvicorn
- [x] Backend: write the hello-world endpoint (`backend/app/main.py`)
- [x] Backend: server runs — JSON at `/`, auto-docs at `/docs`
- [x] Adopt the standard project layout (`app/` package, self-contained subprojects)
- [x] Frontend: scaffold the React app with Vite
- [x] Frontend: install dependencies (`npm install`)
- [x] Frontend: dev server runs — starter page + counter at `:5173`
- [x] 💾 commit: *"Step 1: FastAPI + React hello world"*

### Step 2 — First API  ·  *routes, JSON & Pydantic*  ✅
- [x] Routes & HTTP methods; the CRUD ↔ verb map
- [x] REST: URLs name *things* (`/contacts`, `/contacts/{id}`)
- [x] What JSON really is (text; serialize / parse; vs. Python dict)
- [x] Return a list of contacts as JSON
- [x] Define a `Contact` Pydantic model — the data "blueprint"
- [x] FastAPI reads type hints → validates output **and** input
- [x] Read errors: browser `500` vs. the real message in the server log
- [x] HTTP status codes: 2xx / 4xx / 5xx (`200`, `404`, `422`, `500`)
- [x] Path parameters + the get-or-404 pattern (`HTTPException`)
- [x] 💾 commit: *"Step 2: contacts API with Pydantic validation"*

### Step 3 — First React Page  ·  new idea: *UI = f(state)*
- [ ] Learn: components & JSX
- [ ] Learn: `useState` and "UI is a function of state"
- [ ] Fetch the contacts with `fetch()`
- [ ] Learn: `useEffect` & the request lifecycle
- [ ] Hit (and understand!) **CORS** — the cross-origin block
- [ ] Handle loading & error states
- [ ] Render the list on the page
- [ ] 💾 commit

### Step 4 — A Database  ·  new idea: *persistence & CRUD*
- [ ] Learn: what a database is; SQLite = a file
- [ ] Learn: SQLModel = Pydantic model + DB table
- [ ] Create the DB and the `contacts` table
- [ ] Implement **C**reate + **R**ead endpoints
- [ ] Implement **U**pdate + **D**elete endpoints
- [ ] Learn: path params for `/contacts/{id}` against real data
- [ ] Test full CRUD via `/docs`
- [ ] 💾 commit

### Step 5 — The Real App  ·  new idea: *relationships & forms*
- [ ] Backend: add Notes, one-to-many with Contacts
- [ ] Frontend: list view of contacts
- [ ] Frontend: detail view (one contact + its notes)
- [ ] Frontend: a form (controlled inputs)
- [ ] Learn: simple client-side routing (list ↔ detail)
- [ ] Wire create / update / delete from the UI
- [ ] 💾 commit

### Step 6 — Grown-up Concepts  ·  new idea: *structure, auth, migration*
- [ ] Deeper backend structure (routers, services, config, tests/)
- [ ] Auth basics: what a token is, protecting routes
- [ ] Swap manual `fetch()` for TanStack Query
- [ ] Concept: the strangler-fig migration pattern
- [ ] (Optional) add TypeScript to the frontend
- [ ] 💾 commit

---

## 🧠 Concepts unlocked

**Unlocked so far:**
- [x] Client–server model; HTTP request/response
- [x] `localhost` & ports (`:8000` backend, `:5173` frontend)
- [x] Server vs app: **Uvicorn** (the server) runs **FastAPI** (the app)
- [x] Auto-generated interactive API docs (`/docs`)
- [x] How `uv` finds a project (searches *upward*) & how Python imports resolve
- [x] Standard layout: self-contained subprojects; app code in a package (`app/`)
- [x] Two-language repo: `.venv` vs `node_modules`; per-subproject `.gitignore`
- [x] HTTP methods & the CRUD map
- [x] REST: resource-oriented URLs (`/contacts`, `/contacts/{id}`)
- [x] JSON: a *text* format; serialize (Python→JSON) / parse (JSON→objects)
- [x] Pydantic models & response validation
- [x] FastAPI reads type hints → validates **input and output**
- [x] Path parameters
- [x] HTTP status codes (2xx / 4xx / 5xx)
- [x] The get-or-404 pattern (`HTTPException`)
- [x] Debugging: a browser `500` → go read the server log

**Coming up:**
- [ ] JSX & components
- [ ] React state (`useState`) & "UI = f(state)"
- [ ] `fetch()` & CORS
- [ ] SQLModel & SQLite CRUD
- [ ] One-to-many relationships
- [ ] Forms & controlled inputs
- [ ] Auth & tokens

---

## 📓 Log

Jot a line here whenever something clicks or bites — future-you will thank you.

- **Step 1:** Adopted the standard layout — `backend/` and `frontend/` are each
  self-contained subprojects. Backend code lives in the `app/` package; run it from
  inside `backend/` with `uvicorn app.main:app --reload`.
- **Step 2:** Built the API — `GET /contacts` (the list) and `GET /contacts/{id}` (one).
  Learned what JSON actually is, added a `Contact` Pydantic model so bad data can't slip
  through, and the get-or-404 pattern. Rule that stuck: a browser `500` → read the server
  terminal for the real error.
```
