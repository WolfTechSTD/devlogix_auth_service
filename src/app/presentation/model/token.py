from dataclasses import dataclass
from typing import Self

from app.application.model.token import RedisTokenView


@dataclass
class JsonCookieToken:
    key: str
    token: str
    lifetime_seconds: int

    @classmethod
    def from_into(cls, source: RedisTokenView) -> Self:
        return cls(
            key=source.key,
            token=source.token,
            lifetime_seconds=source.lifetime_seconds
        )
