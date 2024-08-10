from abc import abstractmethod

from app.kernel.model.id import Id
from app.kernel.model.user import User, NewUser, UpdateUser
from .base import Repository


class UserRepository(Repository[NewUser, UpdateUser, User]):
    @abstractmethod
    async def get_total(self) -> int: ...

    @abstractmethod
    async def check_user(self, username: str, email: str) -> bool: ...

    @abstractmethod
    async def check_user_exists(self, user_id: Id) -> bool: ...

    @abstractmethod
    async def check_username_exists(
            self,
            user_id: Id,
            username: str
    ) -> bool: ...

    @abstractmethod
    async def check_email_exists(
            self,
            user_id: Id,
            email: str
    ) -> bool: ...

    @abstractmethod
    async def get_user(
            self,
            username: str | None,
            email: str | None) -> User | None: ...
