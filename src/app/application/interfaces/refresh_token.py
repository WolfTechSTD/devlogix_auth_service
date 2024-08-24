from abc import abstractmethod
from typing import Protocol

from app.domain.model.jwt import RefreshToken


class RefreshTokenGateway(Protocol):
    @abstractmethod
    async def insert(self, source: RefreshToken) -> RefreshToken: ...

    @abstractmethod
    async def update(self, source: RefreshToken) -> RefreshToken: ...

    @abstractmethod
    async def get(self, name: str) -> RefreshToken | None: ...

    @abstractmethod
    async def check_user_token(self, name: str) -> bool: ...

    @abstractmethod
    async def check_token(self, name: str) -> bool: ...
