from typing import Self

from pydantic import Field

from app.application.model.user import CreateUserView, UserView
from .base import Base


class JsonUser(Base):
    id: str = Field(..., description="Уникальный идентификатор")
    username: str = Field(..., description="Юзернейм")
    email: str = Field(..., description="E-mail")

    @classmethod
    def into(cls, value: UserView) -> Self:
        return JsonUser(
            id=value.id,
            username=value.username,
            email=value.email
        )


class JsonCreateUser(Base):
    username: str = Field(..., description="Юзернейм")
    email: str = Field(..., description="E-mail")
    password: str = Field(..., description='Пароль')

    @classmethod
    def into(cls, value: Self) -> CreateUserView:
        return CreateUserView(
            username=value.username,
            email=value.email,
            password=value.password
        )
