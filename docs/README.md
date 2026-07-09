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

## Steps

| # | Doc | What you'll understand |
|---|---|---|
| 1 | [Setup & Hello World](step-1-setup-and-hello-world.md) | The two-process model; project structure |
| 2 | [First API](step-2-first-api.md) | Routes, JSON, Pydantic validation, status codes |
| 3 | [First React Page](step-3-first-react-page.md) | Components, state, fetching, CORS |
| 4 | *A Database* (coming) | Persistence, SQLModel, CRUD |
| 5 | *The Real App* (coming) | Relationships, forms, detail views |
| 6 | *Grown-up Concepts* (coming) | Auth, structure, migration |
