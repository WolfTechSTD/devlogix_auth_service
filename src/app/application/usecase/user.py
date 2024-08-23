from typing import cast

from app.application.exceptions import (
    UserExistsException,
    UserLoginException,
    UserWithEmailAndUsernameExistsException,
    UserWithEmailExistsException,
    UserWithUsernameExistsException,
    InvalidTokenException,
    UserNotFoundException,
)
from app.application.interfaces import (
    UoW,
    UserGateway,
    BaseStrategy,
    UserPermission,
    APasswordProvider,
)
from app.application.model.token import RedisTokenView
from app.application.model.user import (
    CreateUserView,
    UserView,
    UserLoginView,
    UpdateUserView,
    UpdateUserMeView,
    UserListView,
)
from app.domain.model.id import Id
from app.domain.model.token import RedisToken


class UserUseCase:
    def __init__(
            self,
            uow: UoW,
            user_gateway: UserGateway,
            password_provider: APasswordProvider,
            strategy_redis: BaseStrategy,
            user_permission: UserPermission | None
    ) -> None:
        self.user_gateway = user_gateway
        self.uow = uow
        self.password_provider = password_provider
        self.strategy_redis = strategy_redis
        self.user_permission = user_permission

    async def create_user(self, source: CreateUserView) -> UserView:
        if await self.user_gateway.check_user(
                username=source.username,
                email=source.email
        ):
            raise UserExistsException()
        source.password = self.password_provider.get_hash(source.password)
        user = await self.user_gateway.insert(source.into())
        await self.uow.commit()
        return UserView.from_into(user)

    async def login(self, source: UserLoginView) -> RedisTokenView:
        user = await self.user_gateway.get_user(source.username, source.email)

        if user is None:
            raise UserLoginException()

        if not self.password_provider.verify_password(
                source.password,
                user.password
        ):
            raise UserLoginException()

        source = source.create_token(user)
        token = await self.strategy_redis.write(source.into("cookie"))
        token.value = source.token
        return RedisTokenView.from_into(token)

    async def update_user(
            self,
            source: UpdateUserView,
            token: str
    ) -> UserView:
        await self._check_token(token)

        if not await self.user_gateway.check_user_exists(cast(Id, source.id)):
            raise UserNotFoundException()

        await self._check_username_and_email(source)
        await self._set_password_hash(source)

        user = await self.user_gateway.update(source.into())
        await self.uow.commit()
        return UserView.from_into(user)

    async def update_user_me(
            self,
            source: UpdateUserMeView,
            token: str
    ) -> UserView:
        user_id = await self._get_user_id(token)

        if user_id is None:
            raise InvalidTokenException()
        await self._check_username_and_email(source, cast(Id, user_id))
        await self._set_password_hash(source)

        user = await self.user_gateway.update(source.into(cast(Id, user_id)))
        await self.uow.commit()
        return UserView.from_into(user)

    async def get_user(self, user_id: str, token: str) -> UserView:
        await self._check_token(token)
        user = await self.user_gateway.get(cast(Id, user_id))

        if user is None:
            raise UserNotFoundException()

        return UserView.from_into(user)

    async def get_users(
            self,
            limit: int,
            offset: int,
            token: str
    ) -> UserListView:
        await self._check_token(token)
        users = await self.user_gateway.get_list(
            limit=limit,
            offset=limit * offset
        )
        total = await self.user_gateway.get_total()
        return UserListView(
            total=total,
            values=(UserView.from_into(user) for user in users)
        )

    async def get_user_me(self, token: str) -> UserView:
        user_id = await self._get_user_id(token)

        if user_id is None:
            raise InvalidTokenException()

        user = await self.user_gateway.get(cast(Id, user_id))

        if user is None:
            raise InvalidTokenException()

        return UserView.from_into(user)

    async def delete_user_me(self, token: str) -> None:
        user_id = await self._get_user_id(token)

        if user_id is None:
            raise InvalidTokenException()

        await self.user_gateway.delete(cast(id, user_id))
        await self.uow.commit()

    async def logout(self, token: str) -> None:
        await self._check_token(token)
        await self._destroy_token(token)

    async def _check_username_and_email(
            self,
            source: UpdateUserView | UpdateUserMeView,
            user_id: Id | None = None
    ) -> None:
        err = {
            "username": await self.user_gateway.check_username_exists(
                id=user_id or cast(Id, source.id),
                username=source.username or ""
            ),
            "email": await self.user_gateway.check_email_exists(
                id=user_id or cast(Id, source.id),
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
            source.password = self.password_provider.get_hash(source.password)

    async def _check_token(self, token: str) -> None:
        await self.user_permission.check_token(
            RedisToken(key=f"cookie::{token}")
        )

    async def _get_user_id(self, token: str) -> str:
        return await self.user_permission.get_user_id(
            RedisToken(key=f"cookie::{token}")
        )

    async def _destroy_token(self, token: str) -> None:
        await self.user_permission.logout(
            RedisToken(key=f"cookie::{token}")
        )
