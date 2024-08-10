from typing import cast

from app.application.exceptions import (
    UserExistsException,
    UserNotFoundException,
    UserWithUsernameExistsException,
    UserWithEmailExistsException,
)
from app.application.model.user import (
    CreateUserView,
    UserView,
    UserListView,
    UpdateUserView,
)
from app.kernel.model.id import Id
from app.kernel.repository.user import UserRepository
from app.kernel.security.password import PasswordProvider


class UserUseCase:
    def __init__(
            self,
            repository: UserRepository,
            password_provider: PasswordProvider
    ) -> None:
        self.repository = repository
        self.password_provider = password_provider

    async def create_user(self, source: CreateUserView) -> UserView:
        if await self.repository.check_user(
                username=source.username,
                email=source.email
        ):
            raise UserExistsException()
        source.password = self.password_provider.get_password_hash(
            source.password
        )
        user = await self.repository.insert(source.into())
        await self.repository.save()
        return UserView.from_into(user)

    async def update_user(self, source: UpdateUserView) -> UserView:
        if not await self.repository.check_user_exists(cast(Id, source.id)):
            raise UserNotFoundException()

        if await self.repository.check_username_exists(
                user_id=cast(Id, source.id),
                username=source.username or ""
        ):
            raise UserWithUsernameExistsException()

        if await self.repository.check_email_exists(
                cast(Id, source.id),
                source.email or ""
        ):
            raise UserWithEmailExistsException()

        if source.password is not None:
            source.password = self.password_provider.get_password_hash(
                source.password
            )

        user = await self.repository.update(source.into())
        await self.repository.save()
        return UserView(
            id=str(user.id),
            username=user.username,
            email=user.email,
            is_active=user.is_active
        )

    async def get_user(self, user_id: str) -> UserView:
        user = await self.repository.get(cast(Id, user_id))
        if user is None:
            raise UserNotFoundException()
        return UserView(
            id=str(user.id),
            username=user.username,
            email=user.email,
            is_active=user.is_active
        )

    async def get_users(
            self,
            limit: int,
            offset: int
    ) -> UserListView:
        users = await self.repository.get_list(
            limit=limit,
            offset=limit * offset
        )
        total = await self.repository.get_total()
        return UserListView(
            total=total,
            values=(UserView(
                id=str(user.id),
                username=user.username,
                email=user.email,
                is_active=user.is_active
            ) for user in users)
        )
