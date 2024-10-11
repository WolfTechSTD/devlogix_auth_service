from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapter.db.connect import get_transaction
from app.adapter.db.gateway import (
    UserGateway,
    RefreshTokenGateway,
)
from app.application.usecase.auth import AuthUseCase
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
    async def auth_usecase(self) -> AsyncIterator[AuthUseCase]:
        yield AuthUseCase(
            transaction=self.transaction,
            user_gateway=self.user_gateway,
            refresh_token_gateway=self.refresh_token_gateway
        )
