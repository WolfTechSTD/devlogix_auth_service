from abc import abstractmethod
from collections.abc import Iterator
from typing import Protocol, Any

from app.kernel.model.user import User


class UserRepository(Protocol):
    @abstractmethod
    async def create_user(self, **kwargs: Any) -> User: ...

    @abstractmethod
    async def get_user(self, **kwargs: Any) -> User | None: ...

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
