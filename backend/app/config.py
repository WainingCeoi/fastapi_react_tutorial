from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent  # the backend/ folder


class Settings(BaseSettings):
    # anchored to backend/.env regardless of the current working directory
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")

    database_url: str
    frontend_origin: str = "http://localhost:5173"
    # min_length: an empty SECRET_KEY= line in .env would otherwise pass ("" is a str!)
    # and only blow up at login time — fail at startup instead
    secret_key: str = Field(min_length=32)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    db_echo: bool = False  # SQL logging — off by default: it prints INSERTed values (incl. password hashes)


settings = Settings()
