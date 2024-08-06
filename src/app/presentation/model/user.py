from typing import Self

from pydantic import Field

from app.application.model.user import (
    CreateUserView,
    UserView,
    UserListView,
    UpdateUserView,
)
from .base import Base


class JsonUser(Base):
    id: str = Field(..., description="Уникальный идентификатор")
    username: str = Field(..., description="Юзернейм")
    email: str = Field(..., description="E-mail")
    is_active: bool = Field(..., description="Статус пользователя")

    @classmethod
    def from_into(cls, value: UserView) -> Self:
        return JsonUser(
            id=value.id,
            username=value.username,
            email=value.email,
            is_active=value.is_active
        )


class JsonUserList(Base):
    total: int = Field(..., description="Количество записей")
    limit: int = Field(..., description="Лимит записей")
    offset: int = Field(..., description="Текущая страница")
    values: list[JsonUser] = Field(..., description="Пользователи")

    @classmethod
    def from_into(
            cls,
            limit: int,
            offset: int,
            value: UserListView
    ):
        return JsonUserList(
            total=value.total,
            limit=limit,
            offset=offset,
            values=[JsonUser(
                id=user.id,
                username=user.username,
                email=user.email,
                is_active=user.is_active
            ) for user in value.values]
        )


class JsonCreateUser(Base):
    username: str = Field(..., description="Юзернейм")
    email: str = Field(..., description="E-mail")
    password: str = Field(..., description='Пароль')

    def into(self) -> CreateUserView:
        return CreateUserView(
            username=self.username,
            email=self.email,
            password=self.password
        )


class JsonUpdateUser(Base):
    username: str | None = Field(..., description="Юзернейм")
    email: str | None = Field(..., description="E-mail")
    password: str | None = Field(..., description="Пароль")
    is_active: bool | None = Field(..., description="Статус пользователя")

    def into(self, user_id: str) -> UpdateUserView:
        return UpdateUserView(
            id=user_id,
            username=self.username,
            email=self.email,
            password=self.password,
            is_active=self.is_active
        )
