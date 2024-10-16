from typing import Self, Optional

from pydantic import Field, model_validator

from app.application.model.user import (
    UserLoginView,
    CreateUserView,
    UpdateUserView,
)
from app.presentation.model.base import Base


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


class JsonCreateUser(Base):
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
    password: str = Field(
        ...,
        json_schema_extra={
            "title": "password",
            "description": "Пароль",
            "example": "UserPassword"
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

    def into(self) -> CreateUserView:
        return CreateUserView(
            id=self.id,
            username=self.username,
            email=self.email,
            password=self.password,
            is_active=self.is_active
        )


class JsonUpdateUser(Base):
    id: str = Field(
        ...,
        json_schema_extra={
            "title": "id",
            "description": "Уникальный идентификатор",
            "example": "01J4HC5WQB3FK3FA1FMXYVYJ6Y"
        }
    )
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

    def into(self) -> UpdateUserView:
        return UpdateUserView(
            id=self.id,
            username=self.username,
            email=self.email,
            password=self.password,
            is_active=self.is_active,
        )
