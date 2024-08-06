from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel
from app.kernel.model.user import User


class Users(BaseModel):
    id: Mapped[str] = mapped_column(
        primary_key=True,
        nullable=False,
        unique=True,
        autoincrement=False
    )
    username: Mapped[str] = mapped_column(
        unique=True,
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        unique=True,
        nullable=False
    )
    password: Mapped[str] = mapped_column(
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        nullable=False,
        default=True
    )

    def into(self) -> User:
        return User(
            id=self.id,
            username=self.username,
            email=self.email,
            password=self.password,
            is_active=self.is_active
        )
