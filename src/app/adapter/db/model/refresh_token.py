import datetime as dt
from typing import cast, TypeVar

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.adapter.db.model import BaseModel
from app.domain.model.id import Id
from app.domain.model.token import RefreshToken
from app.domain.model.user import User

UserStorage = TypeVar("UserStorage", bound=User)


class RefreshTokenStorage(BaseModel):
    __tablename__ = "refresh_tokens"

    id: Mapped[str] = mapped_column(
        primary_key=True,
        nullable=False,
        unique=True,
        autoincrement=False
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=True
    )
    name: Mapped[str] = mapped_column(
        nullable=False,
        unique=True
    )
    is_valid: Mapped[bool] = mapped_column(
        nullable=False,
        default=True
    )
    date_on: Mapped[dt.datetime] = mapped_column(
        nullable=False,
        default=dt.datetime.now
    )
    user: Mapped["UserStorage"] = relationship()

    def into(self) -> RefreshToken:
        return RefreshToken(
            id=cast(Id, self.id),
            user_id=cast(Id, self.user_id),
            name=self.name,
            is_valid=self.is_valid,
            user=self.user
        )
