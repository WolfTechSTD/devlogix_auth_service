from abc import abstractmethod
from typing import Protocol


class UserPermissions(Protocol):
    @abstractmethod
    async def check_cookie_token(self, token: str | None) -> None: ...

    @abstractmethod
    async def get_user_id(self, token: str | None) -> str | None: ...
