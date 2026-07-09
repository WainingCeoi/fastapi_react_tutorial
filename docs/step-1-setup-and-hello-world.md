# Step 1 — Setup & Hello World

> **Goal:** get a FastAPI backend and a React frontend each running as their own process,
> and understand how a browser talks to a server.

## The big idea: a web app is TWO programs

```
  YOUR LAPTOP  (everything here is "localhost")

   ┌───────────┐   1. "give me the page"     ┌──────────────────┐
   │           │ ──────────────────────────► │   Vite server    │
   │  Browser  │   2. HTML + CSS + JS        │  localhost:5173  │
   │  (Chrome) │ ◄────────────────────────── │    FRONTEND      │
   │           │                             └──────────────────┘
   │           │
   │           │   3. JS calls the API       ┌──────────────────┐
   │           │ ──────────────────────────► │ Uvicorn+FastAPI  │
   │           │   4. JSON                   │  localhost:8000  │
   │           │ ◄────────────────────────── │    BACKEND       │
   └───────────┘                             └──────────────────┘
```

- **Frontend** (React + Vite) — the *looks*. Runs **in the browser**. Served by the Vite dev server on `:5173`.
- **Backend** (FastAPI + Uvicorn) — the *brains & memory*. Runs on a server on `:8000`. Speaks JSON.
- They are **separate programs, in separate languages**, talking over **HTTP**. Two jobs, two toolchains → two dev servers.

## Vocabulary (the words in that diagram)

| Term | Meaning |
|---|---|
| **Server** | a program that waits for *requests* and returns *responses* |
| **Client** | whoever makes the request (here, the browser) |
| **HTTP** | the request/response language of the web |
| **localhost / 127.0.0.1** | "this same computer" |
| **Port** | a numbered door (`:8000`, `:5173`) so servers coexist |
| **API** | an interface a program exposes for *other programs* to call |
| **JSON** | a text format for structured data (looks like a Python dict) |
| **Dev server** | a server you run while developing; auto-reloads on save |

## The backend: FastAPI + Uvicorn

- **FastAPI** = the framework (your instructions). **Uvicorn** = the web server (the engine that runs them).
- Minimal app — `backend/app/main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, world"}
```

- `@app.get("/")` registers the function as the handler for `GET /`. Returning a dict → FastAPI **serializes** it to JSON.
- Run it (from `backend/`): `uv run uvicorn app.main:app --reload`
- Free gift: interactive docs at **`/docs`**, generated from your code.

## Project structure: a monorepo of self-contained subprojects

```
fastapi_react_tutorial/       ← git repo (the monorepo root)
├── README.md  .gitignore     ← repo-level (OS junk only)
├── backend/                  ← self-contained PYTHON project
│   ├── pyproject.toml  uv.lock  .python-version  .venv/  .gitignore
│   └── app/                  ← the application PACKAGE
│       ├── __init__.py       ← marks app/ as importable
│       └── main.py
└── frontend/                 ← self-contained JS project
    ├── package.json  node_modules/  .gitignore
    └── src/
```

- Two languages → **two independent projects**. Each has its own deps and `.gitignore`, and each can run, test, and deploy on its own.
- Backend **code** lives in the `app/` **package** (a folder Python can import from); project **metadata** sits at the `backend/` root beside it.

## Decoding `uv run uvicorn app.main:app`

```
uvicorn  app.main : app
         └──┬───┘   └┬┘
            │        └─ the variable `app` (app = FastAPI()) inside that module
            └─ import path: the app/ PACKAGE → its main.py MODULE
```

- `uv` finds a project by searching **upward** for `pyproject.toml` — so you run from inside `backend/`.
- The two "app"s are different things: `app/` (a folder/package) and `app` (the FastAPI object). The command only resolves because you're standing in `backend/`.

## Git: commit the source, not the artifacts

| ✅ Commit (source) | ❌ Never commit (artifacts) |
|---|---|
| code, config | `.venv/` (Python deps) |
| **lockfiles** (`uv.lock`, `package-lock.json`) | `node_modules/` (JS deps) |
| | `__pycache__/`, build output |

- Mental model: the **lockfile is the recipe**; `.venv`/`node_modules` are the **cooked meal**. Version the recipe — anyone can re-cook it with `uv sync` / `npm install`.
- `git check-ignore -v <path>` tells you *which* rule is hiding a path.

## Key takeaways

- A web app is **two processes talking over HTTP**.
- **Uvicorn** (server) runs **FastAPI** (app); `app.main:app` tells it where the app object lives.
- Structure **by language**: self-contained `backend/` and `frontend/`.
- Commit the recipe, not the meal.

---
**Next → [Step 2 — First API](step-2-first-api.md)**
