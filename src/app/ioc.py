from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated

from litestar.params import Dependency

from app.adapter.authentication.strategy import RedisStrategy
from app.adapter.db.gateway import UserGateway
from app.adapter.db.gateway.refresh_token import RefreshTokenGateway
from app.adapter.permission import UserPermission
from app.adapter.security import PasswordProvider, JWTProvider
from app.application.interfaces import Transaction
from app.application.usecase.jwt import JWTUseCase
from app.application.usecase.user import UserUseCase
from app.presentation.interactor import InteractorFactory


class IoC(InteractorFactory):
    def __init__(
            self,
            transaction: Annotated[
                Transaction,
                Dependency(skip_validation=True)
            ],
            user_gateway: UserGateway,
            password_provider: PasswordProvider,
            strategy: RedisStrategy,
            refresh_token_gateway: RefreshTokenGateway,
            jwt_provider: JWTProvider
    ) -> None:
        self.transaction = transaction
        self.user_gateway = user_gateway
        self.password_provider = password_provider
        self.strategy = strategy
        self.refresh_token_gateway = refresh_token_gateway
        self.jwt_provider = jwt_provider

    @asynccontextmanager
    async def user_usecase(
            self,
            user_permissions: UserPermission | None = None
    ) -> AsyncIterator[UserUseCase]:
        yield UserUseCase(
            transaction=self.transaction,
            user_gateway=self.user_gateway,
            password_provider=self.password_provider,
            strategy_redis=self.strategy,
            user_permission=user_permissions
        )

    @asynccontextmanager
    async def jwt_usecase(self) -> AsyncIterator[JWTUseCase]:
        yield JWTUseCase(
            transaction=self.transaction,
            refresh_token_gateway=self.refresh_token_gateway,
            user_gateway=self.user_gateway,
            jwt_provider=self.jwt_provider,
            password_provider=self.password_provider
        )
