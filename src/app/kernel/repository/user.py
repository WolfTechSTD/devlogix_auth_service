from abc import abstractmethod
from typing import Protocol, Any

from app.kernel.model.user import User


class UserRepository(Protocol):
    @abstractmethod
    async def create_user(self, **kwargs: Any) -> User: ...
