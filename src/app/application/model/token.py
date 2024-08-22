from dataclasses import dataclass
from typing import Self

from app.domain.model.id import Id
from app.domain.model.token import RedisToken

LIFETIME = 2592000


@dataclass(slots=True)
class RedisTokenView:
    key: str
    token: str
    lifetime_seconds: int

    @classmethod
    def from_into(cls, source: RedisToken) -> Self:
        return cls(
            "session",
            source.value,
            LIFETIME
        )


@dataclass(slots=True)
class CreateRedisTokenView:
    token: str
    user_id: Id

    def into(self, key: str) -> RedisToken:
        return RedisToken(
            key=f"{key}::{self.token}",
            value=str(self.user_id),
            lifetime_second=LIFETIME
        )
