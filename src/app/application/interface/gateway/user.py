from abc import abstractmethod
from typing import Protocol

from app.domain.model.user import User


class IUserGateway(Protocol):
    @abstractmethod
    async def get(
            self,
            username: str | None,
            email: str | None
    ) -> User | None: ...
