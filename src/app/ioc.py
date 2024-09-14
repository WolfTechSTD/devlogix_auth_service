from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapter.db.connect import get_transaction
from app.adapter.db.gateway import (
    UserGateway,
    RefreshTokenGateway,
)
from app.application.interfaces import IUserPermission
from app.application.usecase.jwt.delete_refresh_token import DeleteRefreshToken
from app.application.usecase.jwt.get_tokens import GetTokens
from app.application.usecase.jwt.update_accesss_token import UpdateAccessToken
from app.application.usecase.jwt.update_refresh_token import UpdateRefreshToken
from app.application.usecase.user.create_user import CreateUser
from app.application.usecase.user.delete_user_me import DeleteUserMe
from app.application.usecase.user.get_user import GetUser
from app.application.usecase.user.get_user_me import GetUserMe
from app.application.usecase.user.get_users import GetUsers
from app.application.usecase.user.update_user import UpdateUser
from app.application.usecase.user.update_user_me import UpdateUserMe
from app.presentation.interactor import InteractorFactory


class IoC(InteractorFactory):
    def __init__(
            self,
            session: AsyncSession,
            refresh_token_time: int
    ) -> None:
        self.transaction = get_transaction(session)
        self.user_gateway = UserGateway(session)
        self.refresh_token_gateway = RefreshTokenGateway(
            session,
            refresh_token_time
        )

    @asynccontextmanager
    async def create_user(
            self,
            user_permission: IUserPermission
    ) -> AsyncIterator[CreateUser]:
        yield CreateUser(
            transaction=self.transaction,
            user_gateway=self.user_gateway,
            user_permission=user_permission
        )

    @asynccontextmanager
    async def get_tokens(
            self,
            user_permission: IUserPermission
    ) -> AsyncIterator[GetTokens]:
        yield GetTokens(
            transaction=self.transaction,
            user_permission=user_permission,
            user_gateway=self.user_gateway,
            refresh_token_gateway=self.refresh_token_gateway,
        )

    @asynccontextmanager
    async def update_access_token(
            self,
            user_permission: IUserPermission
    ) -> AsyncIterator[UpdateAccessToken]:
        yield UpdateAccessToken(
            transaction=self.transaction,
            user_permission=user_permission,
            refresh_token_gateway=self.refresh_token_gateway,
        )

    @asynccontextmanager
    async def update_refresh_token(
            self,
            user_permission: IUserPermission
    ) -> AsyncIterator[UpdateRefreshToken]:
        yield UpdateRefreshToken(
            transaction=self.transaction,
            user_permission=user_permission,
            refresh_token_gateway=self.refresh_token_gateway,
        )

    @asynccontextmanager
    async def delete_refresh_token(self) -> AsyncIterator[DeleteRefreshToken]:
        yield DeleteRefreshToken(
            transaction=self.transaction,
            refresh_token_gateway=self.refresh_token_gateway,
        )

    @asynccontextmanager
    async def get_user_me(self) -> AsyncIterator[GetUserMe]:
        yield GetUserMe(
            user_gateway=self.user_gateway,
        )

    @asynccontextmanager
    async def update_user_me(
            self,
            user_permission: IUserPermission
    ) -> AsyncIterator[UpdateUserMe]:
        yield UpdateUserMe(
            transaction=self.transaction,
            user_permission=user_permission,
            user_gateway=self.user_gateway,
        )

    @asynccontextmanager
    async def delete_user_me(self) -> AsyncIterator[DeleteUserMe]:
        yield DeleteUserMe(
            transaction=self.transaction,
            user_gateway=self.user_gateway,
        )

    @asynccontextmanager
    async def update_user(
            self,
            user_permission: IUserPermission
    ) -> AsyncIterator[UpdateUser]:
        yield UpdateUser(
            transaction=self.transaction,
            user_permission=user_permission,
            user_gateway=self.user_gateway,
        )

    @asynccontextmanager
    async def get_user(self) -> AsyncIterator[GetUser]:
        yield GetUser(
            user_gateway=self.user_gateway
        )

    @asynccontextmanager
    async def get_users(self) -> AsyncIterator[GetUsers]:
        yield GetUsers(
            user_gateway=self.user_gateway,
        )
