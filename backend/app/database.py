from typing import Annotated

from fastapi import Depends
from sqlalchemy import event
from sqlmodel import Session, create_engine

from app.config import settings

engine = create_engine(settings.database_url, echo=settings.db_echo)

if engine.url.get_backend_name() == "sqlite":
    # SQLite ships with foreign-key enforcement OFF per connection — turn it on,
    # so a Note can never point at a contact_id that doesn't exist.
    @event.listens_for(engine, "connect")
    def _enable_sqlite_foreign_keys(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
