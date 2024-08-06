from typing import cast

from app.application.exceptions import (
    UserExistsException,
    UserNotFoundException,
)
from app.application.model.user import CreateUserView, UserView, UserListView
from app.kernel.model.user_id import UserId
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
        user = await self.repository.insert(source.into())
        await self.repository.save()
        return UserView.from_into(user)

    async def get_user(self, user_id: str) -> UserView:
        user = await self.repository.get(cast(UserId, user_id))
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
    ) -> UserListView:
        users = await self.repository.get_users(
            limit=limit,
            offset=limit * offset
        )
        total = await self.repository.get_total()
        return UserListView(
            total=total,
            values=(UserView(
                id=str(user.id),
                username=user.username,
                email=user.email
            ) for user in users)
        )
