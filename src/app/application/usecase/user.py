from typing import cast

from app.application.exceptions import (
    UserExistsException,
    UserNotFoundException,
    UserLoginException,
    UserWithEmailAndUsernameExistsException,
    UserWithEmailExistsException,
    UserWithUsernameExistsException,
    InvalidTokenException,
)
from app.application.model.cookie_token import (
    CookieTokenView,
)
from app.application.model.user import (
    CreateUserView,
    UserView,
    UserListView,
    UpdateUserView,
    UserLoginView,
    UpdateUserMeView,
)
from app.kernel.model.id import Id
from app.kernel.permissions.user import UserPermissions
from app.kernel.repository.cookie_token import CookieTokenRepository
from app.kernel.repository.user import UserRepository
from app.kernel.security.password import PasswordProvider


class UserUseCase:
    def __init__(
            self,
            repository: UserRepository,
            password_provider: PasswordProvider,
            cookie_token_repository: CookieTokenRepository,
            user_permissions: UserPermissions | None
    ) -> None:
        self.repository = repository
        self.password_provider = password_provider
        self.cookie_token_repository = cookie_token_repository
        self.user_permissions = user_permissions

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
        await self.user_permissions.check_cookie_token(source.token)

        if not await self.repository.check_user_exists(cast(Id, source.id)):
            raise UserNotFoundException()

        await self._check_username_and_email(source)
        await self._set_password_hash(source)

        user = await self.repository.update(source.into())
        await self.repository.save()
        return UserView(
            id=str(user.id),
            username=user.username,
            email=user.email,
            is_active=user.is_active
        )

    async def update_user_me(self, source: UpdateUserMeView) -> UserView:
        user_id = await self.user_permissions.get_user_id(source.token)

        if user_id is None:
            raise InvalidTokenException()
        await self._check_username_and_email(source, cast(Id, user_id))
        await self._set_password_hash(source)

        user = await self.repository.update(source.into(cast(Id, user_id)))
        await self.repository.save()
        return UserView(
            id=str(user.id),
            username=user.username,
            email=user.email,
            is_active=user.is_active
        )

    async def get_user(self, user_id: str, token: str) -> UserView:
        await self.user_permissions.check_cookie_token(token)
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
            offset: int,
            token: str
    ) -> UserListView:
        await self.user_permissions.check_cookie_token(token)
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

    async def get_user_me(self, token: str) -> UserView:
        user_id = await self.user_permissions.get_user_id(token)

        if user_id is None:
            raise InvalidTokenException()

        user = await self.repository.get(cast(Id, user_id))

        if user is None:
            raise InvalidTokenException()

        return UserView(
            id=str(user.id),
            username=user.username,
            email=user.email,
            is_active=user.is_active
        )

    async def _check_username_and_email(
            self,
            source: UpdateUserView | UpdateUserMeView,
            user_id: Id | None = None
    ) -> None:
        err = {
            "username": await self.repository.check_username_exists(
                user_id=user_id or cast(Id, source.id),
                username=source.username or ""
            ),
            "email": await self.repository.check_email_exists(
                user_id=user_id or cast(Id, source.id),
                email=source.email or ""
            )
        }

        if err["email"] and err["username"]:
            raise UserWithEmailAndUsernameExistsException()
        elif err["email"]:
            raise UserWithEmailExistsException()
        elif err["username"]:
            raise UserWithUsernameExistsException()

    async def _set_password_hash(
            self,
            source: UpdateUserView | UpdateUserMeView
    ) -> None:
        if source.password is not None:
            source.password = self.password_provider.get_password_hash(
                source.password
            )
