import os
from dataclasses import dataclass

from app.exceptions import ConfigParseError


@dataclass
class DatabaseConfig:
    db_url: str


@dataclass
class JWTConfig:
    secret_key: str
    algorithm: str
    access_token_time: int
    refresh_token_time: int


@dataclass
class KafkaConfig:
    url: str


@dataclass
class CORSConfig:
    allow_origins: list[str]


@dataclass
class ApplicationConfig:
    debug: bool
    db: DatabaseConfig
    jwt: JWTConfig
    cors: CORSConfig
    kafka: KafkaConfig


def get_str_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ConfigParseError(f"{key} must be set")
    return value


def _load_kafka_config() -> KafkaConfig:
    return KafkaConfig(
        url=get_str_env("KAFKA_URL"),
    )


def load_database_config() -> DatabaseConfig:
    return DatabaseConfig(db_url=get_str_env("DATABASE_URL"))


def load_config() -> ApplicationConfig:
    return ApplicationConfig(
        debug=True if get_str_env("DEBUG") in ("true", "True") else False,
        db=load_database_config(),
        jwt=_load_jwt_config(),
        cors=_load_cors_config(),
        kafka=_load_kafka_config(),
    )


def _load_cors_config() -> CORSConfig:
    return CORSConfig(
        allow_origins=get_str_env("ALLOW_ORIGINS").split(","),
    )


def _load_jwt_config() -> JWTConfig:
    return JWTConfig(
        secret_key=get_str_env("SECRET_KEY"),
        algorithm=get_str_env("ALGORITHM"),
        access_token_time=int(get_str_env("ASSESS_TOKEN_TIME")),
        refresh_token_time=int(get_str_env("REFRESH_TOKEN_TIME")),
    )
