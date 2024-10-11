from abc import abstractmethod
from typing import Protocol, TypeVar

from app.domain.model.id import Id
from app.domain.model.user import User


class IUserPermission(Protocol):
    @abstractmethod
    async def change_password(
            self,
            source: User,
    ) -> None: ...

    @abstractmethod
    async def get_access_token(self, user_id: Id) -> str: ...

    @abstractmethod
    async def get_refresh_token(self) -> str: ...
