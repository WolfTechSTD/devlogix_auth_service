import os
from dataclasses import dataclass

from .exceptions import ConfigParseError


@dataclass
class DatabaseConfig:
    db_url: str


@dataclass
class ApplicationConfig:
    debug: bool
    db: DatabaseConfig


def get_str_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ConfigParseError(f"{key} must be set")
    return value


def _load_database_config() -> DatabaseConfig:
    return DatabaseConfig(db_url=os.getenv("DATABASE_URL"))


def load_config() -> ApplicationConfig:
    return ApplicationConfig(
        debug=True if get_str_env("DEBUG") in ("true", "True") else False,
        db=_load_database_config()
    )
