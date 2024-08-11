from dataclasses import dataclass
from typing import Self

from app.kernel.model.cookie_token import NewCookieToken, CookieToken
from app.kernel.model.id import Id

LIFETIME = 2592000


@dataclass
class CookieTokenView:
    key: str
    token: str
    lifetime_seconds: int

    @classmethod
    def from_into(cls, source: CookieToken) -> Self:
        return cls(
            "session",
            source.key,
            LIFETIME
        )


@dataclass
class CreateCookieTokenView:
    token: str
    user_id: Id

    def into(self) -> NewCookieToken:
        return NewCookieToken(
            key=self.token,
            value=str(self.user_id),
            lifetime_seconds=LIFETIME
        )
