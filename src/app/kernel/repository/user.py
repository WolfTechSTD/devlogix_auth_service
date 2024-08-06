from abc import abstractmethod
from collections.abc import Iterator
from typing import Protocol

from app.kernel.model.id import Id
from app.kernel.model.user import User, NewUser


class UserRepository(Protocol):
    @abstractmethod
    async def insert(self, source: NewUser) -> User: ...

    @abstractmethod
    async def get(self, source: Id) -> User | None: ...

    @abstractmethod
    async def get_list(
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
