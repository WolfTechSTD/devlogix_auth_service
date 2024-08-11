import os
from dataclasses import dataclass

from .exceptions import ConfigParseError


@dataclass
class DatabaseConfig:
    db_url: str


@dataclass
class JWTConfig:
    secret_key: str
    algorithm: str


@dataclass
class RedisConfig:
    url_cookie_token: str


@dataclass
class ApplicationConfig:
    debug: bool
    db: DatabaseConfig
    jwt: JWTConfig
    redis: RedisConfig


def get_str_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ConfigParseError(f"{key} must be set")
    return value


def _load_redis_config() -> RedisConfig:
    return RedisConfig(url_cookie_token=os.getenv('REDIS_URL_COOKIE_TOKEN'))


def _load_database_config() -> DatabaseConfig:
    return DatabaseConfig(db_url=os.getenv("DATABASE_URL"))


def _load_jwt_config() -> JWTConfig:
    return JWTConfig(
        secret_key=os.getenv("SECRET_KEY"),
        algorithm=os.getenv("ALGORITHM")
    )


def load_config() -> ApplicationConfig:
    return ApplicationConfig(
        debug=True if get_str_env("DEBUG") in ("true", "True") else False,
        db=_load_database_config(),
        jwt=_load_jwt_config(),
        redis=_load_redis_config()
    )
