from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapter.authentication.strategy import RedisStrategy
from app.adapter.db.connect import get_transaction
from app.adapter.db.gateway import (
    UserGateway,
    RefreshTokenGateway,
)
from app.adapter.permission import UserPermission
from app.adapter.security import (
    PasswordProvider,
    JWTProvider,
)
from app.application.usecase.jwt import JWTUseCase
from app.application.usecase.user import UserUseCase
from app.presentation.interactor import InteractorFactory


class IoC(InteractorFactory):
    def __init__(
            self,
            session: AsyncSession,
            password_provider: PasswordProvider,
            strategy: RedisStrategy,
            jwt_provider: JWTProvider,
            refresh_token_time: int
    ) -> None:
        self.transaction = get_transaction(session)
        self.user_gateway = UserGateway(session)
        self.password_provider = password_provider
        self.strategy = strategy
        self.refresh_token_gateway = RefreshTokenGateway(session, refresh_token_time)
        self.jwt_provider = jwt_provider

    @asynccontextmanager
    async def user_usecase(
            self,
            user_permission: UserPermission | None = None
    ) -> AsyncIterator[UserUseCase]:
        yield UserUseCase(
            transaction=self.transaction,
            user_gateway=self.user_gateway,
            password_provider=self.password_provider,
            strategy_redis=self.strategy,
            user_permission=user_permission
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
