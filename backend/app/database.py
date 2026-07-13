from typing import Annotated

from fastapi import Depends
from sqlalchemy import event
from sqlmodel import Session, create_engine

from app.config import settings


def enable_sqlite_foreign_keys(engine):
    # SQLite ships with FK enforcement OFF per connection — turn it on, so a Note can
    # never point at a missing contact. Tests must call this on their own engine too,
    # or they'd silently run a different configuration than production.
    if engine.url.get_backend_name() != "sqlite":
        return

    @event.listens_for(engine, "connect")
    def _fk_on(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


engine = create_engine(settings.database_url, echo=settings.db_echo)
enable_sqlite_foreign_keys(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
