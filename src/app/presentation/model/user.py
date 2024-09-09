from typing import Self, Optional

from pydantic import Field, model_validator

from app.application.model.user import (
    CreateUserView,
    UserView,
    UserListView,
    UpdateUserView,
    UserLoginView,
    UpdateUserMeView,
)
from app.presentation.constants import TOTAL, LIMIT, OFFSET
from app.presentation.model.base import Base


class JsonUser(Base):
    id: str = Field(
        ...,
        json_schema_extra={
            "title": "id",
            "description": "Уникальный идентификатор",
            "example": "01J4HC5WQB3FK3FA1FMXYVYJ6Y"
        }
    )
    username: str = Field(
        ...,
        json_schema_extra={
            "title": "username",
            "description": "Юзернейм",
            "example": "User"
        }
    )
    email: str = Field(
        ...,
        json_schema_extra={
            "title": "email",
            "description": "E-mail",
            "example": "operation@gmail.com"
        }
    )
    is_active: bool = Field(
        ...,
        json_schema_extra={
            "title": "isActive",
            "description": "Статус пользователя",
            "example": True
        }
    )

    @classmethod
    def from_into(cls, value: UserView) -> Self:
        return JsonUser(
            id=value.id,
            username=value.username,
            email=value.email,
            is_active=value.is_active
        )


class JsonUserList(Base):
    total: int = Field(
        ...,
        json_schema_extra={
            "title": "total",
            "description": "Количество записей",
            "example": TOTAL
        }
    )
    limit: int = Field(
        ...,
        json_schema_extra={
            "title": "limit",
            "description": "Лимит записей",
            "example": LIMIT
        }
    )
    offset: int = Field(
        ...,
        json_schema_extra={
            "title": "offset",
            "description": "Текущая страница",
            "example": OFFSET
        }
    )
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
            values=[JsonUser.from_into(user) for user in value.users]
        )


class JsonCreateUser(Base):
    username: str = Field(
        ...,
        json_schema_extra={
            "title": "username",
            "description": "Юзернейм",
            "example": "User"
        }
    )
    email: str = Field(
        ...,
        json_schema_extra={
            "title": "email",
            "description": "E-mail",
            "example": "operation@gmail.com"
        }
    )
    password: str = Field(
        ...,
        json_schema_extra={
            "title": "password",
            "description": "Пароль",
            "example": "UserPassword"
        }
    )

    def into(self) -> CreateUserView:
        return CreateUserView(
            username=self.username,
            email=self.email,
            password=self.password
        )


class JsonUpdateUserMe(Base):
    username: Optional[str] = Field(
        None,
        json_schema_extra={
            "title": "username",
            "description": "Юзернейм",
        }
    )
    email: Optional[str] = Field(
        None,
        json_schema_extra={
            "title": "email",
            "description": "E-mail",
        }
    )
    password: Optional[str] = Field(
        None,
        json_schema_extra={
            "title": "password",
            "description": "Пароль",
        }
    )

    def into(self) -> UpdateUserMeView:
        return UpdateUserMeView(
            username=self.username,
            email=self.email,
            password=self.password,
        )


class JsonUpdateUser(Base):
    username: Optional[str] = Field(
        None,
        json_schema_extra={
            "title": "username",
            "description": "Юзернейм",
        }
    )
    email: Optional[str] = Field(
        None,
        json_schema_extra={
            "title": "email",
            "description": "E-mail",
        }
    )
    password: Optional[str] = Field(
        None,
        json_schema_extra={
            "title": "password",
            "description": "Пароль",
        }
    )
    is_active: Optional[bool] = Field(
        None,
        json_schema_extra={
            "title": "isActive",
            "description": "Статус пользователя",
        }
    )

    def into(self, user_id: str) -> UpdateUserView:
        return UpdateUserView(
            id=user_id,
            username=self.username,
            email=self.email,
            password=self.password,
            is_active=self.is_active,
        )


class JsonUserLogin(Base):
    username: Optional[str] = Field(
        None,
        json_schema_extra={
            "title": "username",
            "description": "Юзернейм",
        }
    )
    email: Optional[str] = Field(
        None,
        json_schema_extra={
            "title": "email",
            "description": "E-mail",
        }
    )
    password: str = Field(
        ...,
        json_schema_extra={
            "title": "password",
            "description": "Пароль",
        }
    )

    @model_validator(mode="after")
    def check_username_and_email(self) -> Self:
        username = self.username
        email = self.email
        if username is None and email is None:
            raise ValueError(
                "The email or username field should not be blank"
            )
        elif username and email:
            raise ValueError(
                "The email or username field must be filled in"
            )
        return self

    def into(self) -> UserLoginView:
        return UserLoginView(
            username=self.username,
            email=self.email,
            password=self.password,
        )
