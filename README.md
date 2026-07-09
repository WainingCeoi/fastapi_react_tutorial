# 🧭 FastAPI + React — Learning Journey

Building a **Contacts & Notes** app from scratch to genuinely understand modern web
development — backend-first, one concept at a time, code written by hand.

> **How to use this file:** tick a box every time you finish something. The goal is *many
> small wins*. When every box in a step is checked, you've earned the commit at the bottom
> of that step. 🎯

---

## 📍 You are here

**Step 3 of 6 ✅ done — First React Page**   →   next up: **Step 4 — A Database**
`▰▰▰▱▱▱`  ·  **halfway!** · frontend fetches & renders live data from the API

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

Frontend = the looks. Backend = the brains & memory. They talk over **HTTP** (and the
browser guards cross-origin calls with **CORS**).

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
│   ├── uv.lock  .python-version  .venv/  .gitignore
│   └── app/                  ← the application PACKAGE
│       ├── __init__.py
│       └── main.py           ← FastAPI app, models, endpoints, CORS
│
└── frontend/                 ← self-contained JS project
    ├── package.json  node_modules/  .gitignore
    └── src/
        └── App.jsx           ← your React component
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

---

## 🎯 Roadmap

### Step 1 — Setup & Hello World  ·  *client–server model*  ✅
- [x] Confirm the stack & the build target
- [x] Understand the two-process (client–server) model
- [x] Backend: install FastAPI + Uvicorn; write & run the hello-world endpoint
- [x] Adopt the standard project layout (`app/` package, self-contained subprojects)
- [x] Frontend: scaffold with Vite; dev server runs at `:5173`
- [x] 💾 commit: *"Step 1: FastAPI + React hello world"*

### Step 2 — First API  ·  *routes, JSON & Pydantic*  ✅
- [x] Routes & HTTP methods; the CRUD ↔ verb map; REST resource URLs
- [x] What JSON really is (text; serialize / parse; vs. Python dict)
- [x] Return contacts as JSON; define a `Contact` Pydantic model
- [x] FastAPI reads type hints → validates output **and** input
- [x] HTTP status codes (200 / 404 / 422 / 500); read errors in the server log
- [x] Path parameters + the get-or-404 pattern (`HTTPException`)
- [x] 💾 commit: *"Step 2: contacts API with Pydantic validation"*

### Step 3 — First React Page  ·  *UI = f(state)*  ✅
- [x] Components & JSX; one root element; `{ }` to drop JS into markup
- [x] Render a list with `.map()` + `key`
- [x] `useState` — reactive data; the "UI = f(state)" idea
- [x] `useEffect(…, [])` — run a side effect once, after render
- [x] `fetch()` the API; Promises & `.then` / `.catch` / `.finally`
- [x] Same-origin policy & **CORS**; fix with FastAPI `CORSMiddleware`
- [x] The three states of a fetch: **loading / error / success**
- [x] The fetch footgun: it doesn't reject on 4xx/5xx — check `response.ok`
- [x] 💾 commit: *"Step 3: React page fetching and rendering contacts"*

### Step 4 — A Database  ·  new idea: *persistence & CRUD*
- [ ] Learn: what a database is; SQLite = a file
- [ ] Learn: SQLModel = Pydantic model + DB table
- [ ] Create the DB and the `contacts` table
- [ ] Implement **C**reate + **R**ead endpoints
- [ ] Implement **U**pdate + **D**elete endpoints
- [ ] Swap the hardcoded list for real DB queries
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
- [x] Client–server model; HTTP request/response; `localhost` & ports
- [x] Server vs app: **Uvicorn** (server) runs **FastAPI** (app); auto-docs at `/docs`
- [x] How `uv` finds a project & how Python imports resolve
- [x] Standard layout: self-contained subprojects; app code in a package (`app/`)
- [x] Two-language repo: `.venv` vs `node_modules`; per-subproject `.gitignore`
- [x] HTTP methods & the CRUD map; REST resource URLs
- [x] JSON: a *text* format; serialize (Python→JSON) / parse (JSON→objects)
- [x] Pydantic models; FastAPI validates **input and output** from type hints
- [x] Path parameters; the get-or-404 pattern (`HTTPException`)
- [x] HTTP status codes (2xx / 4xx / 5xx)
- [x] JSX & components; `{ }`, `.map()` + `key`, one root element
- [x] React state (`useState`) & "UI = f(state)"
- [x] `useEffect` + the fetch lifecycle; Promises (`.then`/`.catch`/`.finally`)
- [x] Handling loading / error / success; the `response.ok` footgun
- [x] Same-origin policy, **CORS** & middleware (browser-enforced!)
- [x] Debugging: browser console (frontend) vs. server log (backend)

**Coming up:**
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
  Learned what JSON actually is, added a `Contact` Pydantic model, and the get-or-404
  pattern. Rule that stuck: a browser `500` → read the server terminal for the real error.
- **Step 3:** The frontend came alive — a React page that fetches `/contacts` and renders
  it, with loading + error states. Hit the CORS wall and fixed it with `CORSMiddleware`.
  Big lesson: CORS is **browser-enforced** — the server said `200`, the browser blocked
  the read. Also: `fetch` doesn't reject on 4xx/5xx, so check `response.ok`.
```
