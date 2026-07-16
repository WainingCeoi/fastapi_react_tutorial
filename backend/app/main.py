from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlmodel import Session, SQLModel, select

from app.config import settings
from app.database import engine
from app.model import Contact
from app.routers import contacts, notes, users

# The built frontend (produced by `npm run build` / `make build`). Absent during
# development and tests — the guard below keeps those paths working without it.
FRONTEND_DIST = (Path(__file__).resolve().parents[2] / "frontend" / "dist").resolve()


def seed_data():
    with Session(engine) as session:
        if session.exec(select(Contact)).first() is None:
            session.add(Contact(name="Walter White", email="walter.white@example.com"))
            session.add(
                Contact(name="Jesse Pinkman", email="jesse.pinkman@example.com")
            )
            session.add(Contact(name="Saul Goodman", email="saul.goodman@example.com"))
            session.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: runs once when the SERVER starts (not when the module is imported)
    # — by now `alembic upgrade head` has built the schema
    SQLModel.metadata.create_all(engine)
    seed_data()
    yield  # the app serves requests while parked here
    # shutdown: anything after the yield would run when the server stops


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_methods=["*"],
    allow_headers=["*"],
)

# The JSON API lives under /api so its paths never collide with the React app's
# client-side routes. In the browser, /contacts/1 is a *page* (React Router) while
# /api/contacts/1 is the *data* it fetches — two namespaces, no clash. This is what
# lets one server (`make start`) serve both, refresh-safe.
app.include_router(contacts.router, prefix="/api")
app.include_router(notes.router, prefix="/api")
app.include_router(users.router, prefix="/api")


@app.get("/api")
def api_root():
    return {"message": "Hello, world"}


# Single-server mode: if the frontend has been built, this one process serves it too
# (API + UI on one port, same-origin, no CORS). `make start` builds `dist/` then runs
# this; in plain dev the folder is absent and this whole block is skipped.
if FRONTEND_DIST.is_dir():

    # GET + HEAD (browsers/proxies HEAD pages); hidden from the OpenAPI schema — it
    # serves the UI, it isn't part of the JSON API contract.
    @app.api_route("/{spa_path:path}", methods=["GET", "HEAD"], include_in_schema=False)
    def serve_spa(spa_path: str):
        # An unknown /api/* path is a genuine 404, not a page — don't hand back HTML.
        if spa_path == "api" or spa_path.startswith("api/"):
            raise HTTPException(status_code=404)
        # A real built file (hashed JS/CSS, favicon, …) → serve it as-is. The
        # containment check rejects path-traversal like ../../secret; the try/except
        # turns a malformed path (e.g. an encoded null byte) into a normal response
        # instead of a 500.
        try:
            requested = (FRONTEND_DIST / spa_path).resolve()
            if spa_path and FRONTEND_DIST in requested.parents and requested.is_file():
                return FileResponse(requested)
        except (ValueError, OSError):
            pass
        # Anything else is a client-side route (/, /contacts/1, …) → return the SPA
        # entry point and let React Router render it. Refresh on any URL now works.
        return FileResponse(FRONTEND_DIST / "index.html")
