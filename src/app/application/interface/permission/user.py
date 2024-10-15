from abc import abstractmethod
from typing import Protocol, TypeVar

from app.domain.model.id import Id

BaseModel = TypeVar("BaseModel")


class IUserPermission(Protocol):
    @property
    @abstractmethod
    def time_refresh_token(self) -> int: ...

    @property
    @abstractmethod
    def time_access_token(self) -> int: ...

    @abstractmethod
    async def check_password(
            self,
            password: str,
            hashed_password: str
    ) -> None: ...

    @abstractmethod
    async def get_access_token(self, user_id: Id) -> str: ...

    @abstractmethod
    async def get_refresh_token(self) -> str: ...
