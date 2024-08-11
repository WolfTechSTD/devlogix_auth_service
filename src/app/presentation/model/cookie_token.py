from dataclasses import dataclass
from typing import Self

from app.application.model.cookie_token import CookieTokenView


@dataclass
class JsonCookieToken:
    key: str
    token: str
    lifetime_seconds: int

    @classmethod
    def from_into(cls, source: CookieTokenView) -> Self:
        return cls(
            key=source.key,
            token=source.token,
            lifetime_seconds=source.lifetime_seconds
        )
