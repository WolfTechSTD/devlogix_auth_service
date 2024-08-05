from sqlalchemy.orm import Mapped, mapped_column
from ulid import ULID
from .base import BaseModel


class Users(BaseModel):
    id: Mapped[str] = mapped_column(
        primary_key=True,
        nullable=False,
        unique=True,
        autoincrement=False,
        default=str(ULID())
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
