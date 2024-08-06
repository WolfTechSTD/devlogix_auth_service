from abc import abstractmethod

from app.kernel.model.user import User, NewUser
from .base import Repository


class UserRepository(Repository[NewUser, User]):
    @abstractmethod
    async def get_total(self) -> int: ...

    @abstractmethod
    async def check_user(self, username: str, email: str) -> bool: ...
