from collections.abc import Iterator
from dataclasses import asdict

from app.application.exceptions import (
    UserExistsException,
    UserNotFoundException,
)
from app.application.model.user import CreateUserView, UserView
from app.kernel.repository.user import UserRepository


class UserUseCase:
    def __init__(
            self,
            repository: UserRepository
    ) -> None:
        self.repository = repository

    async def create_user(self, source: CreateUserView) -> UserView:
        if await self.repository.check_user(
                username=source.username,
                email=source.email
        ):
            raise UserExistsException()
        user = await self.repository.create_user(**asdict(source))
        return UserView(
            id=str(user.id),
            username=user.username,
            email=user.email
        )

    async def get_user(self, user_id: str) -> UserView:
        user = await self.repository.get_user(id=user_id)
        if user is None:
            raise UserNotFoundException()
        return UserView(
            id=str(user.id),
            username=user.username,
            email=user.email
        )

    async def get_users(
            self,
            limit: int,
            offset: int
    ) -> tuple[Iterator[UserView], int]:
        users, total = await self.repository.get_users(
            limit=limit,
            offset=limit * offset
        )
        return ((UserView(
            id=str(user.id),
            username=user.username,
            email=user.email
        ) for user in users), 10)
