from abc import abstractmethod
from typing import Protocol

from app.domain.model.user import User


class IUserGateway(Protocol):
    @abstractmethod
    async def insert(self, source: User) -> User: ...

    @abstractmethod
    async def get(
            self,
            username: str | None,
            email: str | None
    ) -> User | None: ...

    @abstractmethod
    async def check_user(self, username: str, email: str) -> bool: ...
