from dataclasses import dataclass
from typing import Self

from app.application.model.jwt import TokensView


@dataclass
class JsonCookieToken:
    access_token: str
    refresh_token: str
    access_token_time: int
    refresh_token_time: int

    @classmethod
    def from_into(
            cls,
            access_token_time: int,
            refresh_token_time: int,
            source: TokensView
    ) -> Self:
        return cls(
            access_token=source.access_token,
            refresh_token=source.refresh_token,
            access_token_time=access_token_time,
            refresh_token_time=refresh_token_time
        )
