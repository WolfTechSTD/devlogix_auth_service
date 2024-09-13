from abc import abstractmethod
from typing import Protocol, TypeVar

from app.domain.model.id import Id

BaseModel = TypeVar("BaseModel")


class IUserPermission(Protocol):
    @abstractmethod
    async def change_password(
            self,
            source: BaseModel,
    ) -> None: ...

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
