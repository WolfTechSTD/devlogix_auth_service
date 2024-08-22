from abc import abstractmethod
from typing import Protocol, TypeVar

ModelToken = TypeVar("ModelToken")


class UserPermissionCookie(Protocol):
    @abstractmethod
    async def check_token(self, source: ModelToken) -> None: ...

    @abstractmethod
    async def get_user_id(self, source: ModelToken) -> str: ...
