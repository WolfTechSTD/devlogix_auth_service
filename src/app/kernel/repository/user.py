from abc import abstractmethod
from collections.abc import Iterator
from typing import Protocol

from app.kernel.model.user import User, NewUser
from app.kernel.model.user_id import UserId


class UserRepository(Protocol):
    @abstractmethod
    async def insert(self, source: NewUser) -> User: ...

    @abstractmethod
    async def get(self, source: UserId) -> User | None: ...

    @abstractmethod
    async def get_users(
            self,
            limit: int,
            offset: int
    ) -> Iterator[User]: ...

    @abstractmethod
    async def get_total(self) -> int: ...

    @abstractmethod
    async def check_user(self, username: str, email: str) -> bool: ...

    @abstractmethod
    async def save(self) -> None: ...
