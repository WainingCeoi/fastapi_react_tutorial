# 📚 Tutorial Docs — FastAPI + React

Step-by-step notes capturing the *why* and the mental models behind each stage of this
project. Written to be **re-read**: skim the diagrams, then the "key concepts."

For the live progress checklist, see the [root README](../README.md).

## The one diagram to remember

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
   │           │   4. JSON                   │  localhost:8000  │
   │           │ ◄────────────────────────── │    BACKEND       │
   └───────────┘                             └──────────────────┘
```

A modern web app is **two programs talking over HTTP**: a **frontend** (the looks, runs in
the browser) and a **backend** (the brains & memory, runs on a server). Everything else is
detail.

## Run it

The repo has a root **`Makefile`** as its universal entrance — `make dev` runs both servers
(the diagram above), `make start` builds the UI and serves it **plus** the API from one
process on `:8000`. Full instructions live in the [root README](../README.md#-run-it).

> **Two servers → one, in production.** In `make start` the backend serves the built React app
> for every path except `/api/…` (which stays the JSON API). Namespacing the API under `/api`
> is what lets a single server host both without their routes colliding — and keeps a refresh
> on a real URL like `/contacts/1` landing on the app.

## Steps

| # | Doc | What you'll understand |
|---|---|---|
| 1 | [Setup & Hello World](step-1-setup-and-hello-world.md) | The two-process model; project structure |
| 2 | [First API](step-2-first-api.md) | Routes, JSON, Pydantic validation, status codes |
| 3 | [First React Page](step-3-first-react-page.md) | Components, state, fetching, CORS |
| 4 | [A Database](step-4-a-database.md) | Persistence, SQLModel, CRUD |
| 5 | [The Real App](step-5-the-real-app.md) | Relationships, forms, detail views |
| 6 | [Backend Architecture](step-6-backend-architecture.md) | Dependency injection, testing, project structure |
| 7 | [Config, Auth & Migrations](step-7-config-auth-migrations.md) | Settings & secrets, password hashing, JWT auth, Alembic migrations, strangler-fig |
