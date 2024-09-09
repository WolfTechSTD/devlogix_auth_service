from typing import Self

from pydantic import Field

from app.application.model.jwt import (
    TokensView,
    UpdateAccessTokenView,
    AccessTokenView,
    UpdateRefreshTokenView,
    RefreshTokenView, DeleteRefreshTokenView,
)
from app.presentation.model.base import Base


class JsonToken(Base):
    token_type: str = Field(
        ...,
        description="Тип токена"
    )
    access_token: str = Field(
        ...,
        description="Токен доступа"
    )
    expires_in: int = Field(
        ...,
        description="Время действия токена"
    )
    refresh_token: str = Field(
        ...,
        description="Токен обновления"
    )

    @classmethod
    def from_into(cls, value: TokensView) -> Self:
        return cls(
            token_type=value.token_type,
            access_token=value.access_token,
            expires_in=value.expires_in,
            refresh_token=value.refresh_token
        )


class JsonUpdateAccessToken(Base):
    refresh_token: str = Field(
        ...,
        description="Токен обновления"
    )

    def into(self) -> UpdateAccessTokenView:
        return UpdateAccessTokenView(
            refresh_token=self.refresh_token
        )


class JsonAccessToken(Base):
    token_type: str = Field(
        ...,
        description="Тип токена"
    )
    access_token: str = Field(
        ...,
        description="Токен доступа"
    )
    expires_in: int = Field(
        ...,
        description="Время действия токена"
    )

    @classmethod
    def from_into(cls, value: AccessTokenView) -> Self:
        return cls(
            token_type=value.token_type,
            access_token=value.access_token,
            expires_in=value.expires_in
        )


class JsonUpdateRefreshToken(Base):
    refresh_token: str = Field(
        ...,
        description="Токен обновления"
    )

    def into(self) -> UpdateRefreshTokenView:
        return UpdateRefreshTokenView(
            refresh_token=self.refresh_token
        )


class JsonRefreshToken(Base):
    refresh_token: str = Field(
        ...,
        description="Токен обновления"
    )

    @classmethod
    def from_into(cls, value: RefreshTokenView) -> Self:
        return cls(
            refresh_token=value.refresh_token
        )


class JsonDeleteRefreshToken(Base):
    refresh_token: str = Field(
        ...,
        description="Токен обновления"
    )

    def into(self) -> DeleteRefreshTokenView:
        return DeleteRefreshTokenView(
            refresh_token=self.refresh_token
        )
