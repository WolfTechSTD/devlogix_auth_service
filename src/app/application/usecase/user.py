from typing import cast

from app.application.exceptions import (
    UserExistsException,
    UserNotFoundException,
    UserWithUsernameExistsException,
    UserWithEmailExistsException,
    UserLoginException,
)
from app.application.model.cookie_token import (
    CookieTokenView,
)
from app.application.model.user import (
    CreateUserView,
    UserView,
    UserListView,
    UpdateUserView, UserLoginView,
)
from app.kernel.model.id import Id
from app.kernel.repository.cookie_token import CookieTokenRepository
from app.kernel.repository.user import UserRepository
from app.kernel.security.password import PasswordProvider


class UserUseCase:
    def __init__(
            self,
            repository: UserRepository,
            password_provider: PasswordProvider,
            cookie_token_repository: CookieTokenRepository
    ) -> None:
        self.repository = repository
        self.password_provider = password_provider
        self.cookie_token_repository = cookie_token_repository

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

    async def login(self, source: UserLoginView) -> CookieTokenView:
        user = await self.repository.get_user(source.username, source.email)
        if user is None:
            raise UserLoginException()
        if not self.password_provider.verify_password(
                source.password,
                user.password
        ):
            raise UserLoginException()
        if source.token is not None:
            await self.cookie_token_repository.destroy(
                source.token
            )
        cookie_token = await self.cookie_token_repository.write(
            source.create_token(user).into()
        )
        return CookieTokenView.from_into(cookie_token)

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
