import datetime as dt
from dataclasses import dataclass
from typing import Self

from app.domain.model.jwt import RefreshToken


@dataclass(slots=True)
class TokensView:
    token_type: str
    access_token: str
    expires_in: int
    refresh_token: str

    @classmethod
    def from_into(cls, access_token: str, refresh_token: str) -> Self:
        return cls(
            token_type="Bearer",
            access_token=access_token,
            expires_in=int(dt.timedelta(minutes=15).total_seconds()),
            refresh_token=refresh_token
        )


@dataclass(slots=True)
class AccessTokenView:
    token_type: str
    access_token: str
    expires_in: int

    @classmethod
    def from_into(cls, access_token: str) -> Self:
        return cls(
            token_type="Bearer",
            access_token=access_token,
            expires_in=int(dt.timedelta(minutes=15).total_seconds()),
        )


@dataclass(slots=True)
class UpdateAccessTokenView:
    refresh_token: str


@dataclass(slots=True)
class UpdateRefreshTokenView:
    refresh_token: str

    def into(self, token: str) -> RefreshToken:
        return RefreshToken(name=token)


@dataclass(slots=True)
class DeleteRefreshTokenView:
    refresh_token: str

    def into(self, token: str) -> RefreshToken:
        return RefreshToken(
            user_id=None,
            name=token,
            is_valid=False
        )


@dataclass(slots=True)
class RefreshTokenView:
    refresh_token: str

    @classmethod
    def from_into(cls, refresh_token: str) -> Self:
        return cls(
            refresh_token=refresh_token
        )
