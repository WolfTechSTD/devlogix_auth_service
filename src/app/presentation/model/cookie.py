import datetime as dt
from dataclasses import dataclass, field
from typing import Literal, Self

from app.application.model.jwt import TokensView

ZERO = 0


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
        source: TokensView,
    ) -> Self:
        return cls(
            access_token=source.access_token,
            refresh_token=source.refresh_token,
            access_token_time=access_token_time,
            refresh_token_time=refresh_token_time,
        )


@dataclass(slots=True, kw_only=True)
class JSONCookieAccessToken:
    name: str = field(default="accessToken")
    access_token: str = field(default="")
    secure: bool = field(default=True)
    httponly: bool = field(default=True)
    samesite: Literal["lax", "strict", "none"] = field(default="lax")
    max_age: int = field(default=ZERO)

    @classmethod
    def from_into(cls, source: JsonCookieToken) -> Self:
        return JSONCookieAccessToken(
            access_token=source.access_token,
            max_age=int(
                dt.timedelta(
                    minutes=source.access_token_time,
                ).total_seconds()
            ),
        )


@dataclass(slots=True, kw_only=True)
class JSONCookieRefreshToken:
    name: str = field(default="refreshToken")
    refresh_token: str = field(default="")
    secure: bool = field(default=True)
    httponly: bool = field(default=True)
    samesite: Literal["lax", "strict", "none"] = field(default="lax")
    max_age: int = field(default=ZERO)

    @classmethod
    def from_into(cls, source: JsonCookieToken) -> Self:
        return JSONCookieRefreshToken(
            refresh_token=source.refresh_token,
            max_age=int(
                dt.timedelta(
                    minutes=source.access_token_time,
                ).total_seconds()
            ),
        )
