from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapter.db.connect import get_transaction
from app.adapter.db.gateway import (
    UserGateway,
    RefreshTokenGateway,
)
from app.application.interfaces import IUserPermission
from app.application.usecase.auth import (
    GetTokens,
    UpdateAccessToken,
    UpdateRefreshToken,
    DeleteRefreshToken,
    CreateUser,
)
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
