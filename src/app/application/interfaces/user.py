from abc import abstractmethod
from collections.abc import Iterator
from typing import Protocol

from app.domain.model.id import Id
from app.domain.model.user import User


class IUserGateway(Protocol):
    @abstractmethod
    async def insert(self, source: User) -> User: ...

    @abstractmethod
    async def update(self, source: User) -> User: ...

    @abstractmethod
    async def get(self, source: Id) -> User | None: ...

    @abstractmethod
    async def get_user(
            self,
            username: str | None,
            email: str | None
    ) -> User | None: ...

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
    async def check_user_exists(self, id: Id) -> bool: ...

    @abstractmethod
    async def check_username_exists(self, id: Id, username: str) -> bool: ...

    @abstractmethod
    async def check_email_exists(self, id: Id, email: str) -> bool: ...

    @abstractmethod
    async def delete(self, source: Id) -> User: ...
