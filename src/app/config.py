import os
from dataclasses import dataclass

from app.exceptions.base import ConfigParseError


@dataclass
class DatabaseConfig:
    db_url: str


@dataclass
class JWTConfig:
    secret_key: str
    algorithm: str
    assess_token_time: int
    refresh_token_time: int


@dataclass
class ApplicationConfig:
    debug: bool
    db: DatabaseConfig
    jwt: JWTConfig


def get_str_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ConfigParseError(f"{key} must be set")
    return value


def load_database_config() -> DatabaseConfig:
    return DatabaseConfig(db_url=get_str_env("DATABASE_URL"))


def _load_jwt_config() -> JWTConfig:
    return JWTConfig(
        secret_key=get_str_env("SECRET_KEY"),
        algorithm=get_str_env("ALGORITHM"),
        assess_token_time=int(get_str_env("ASSESS_TOKEN_TIME")),
        refresh_token_time=int(get_str_env("REFRESH_TOKEN_TIME"))
    )


def load_config() -> ApplicationConfig:
    return ApplicationConfig(
        debug=True if get_str_env("DEBUG") in ("true", "True") else False,
        db=load_database_config(),
        jwt=_load_jwt_config(),
    )
