from typing import Self, Optional

from pydantic import Field, model_validator

from app.application.model.user import (
    CreateUserView,
    UserLoginView,
)
from app.presentation.model.base import Base


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
