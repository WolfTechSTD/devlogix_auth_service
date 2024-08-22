from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated

from litestar.params import Dependency

from app.adapter.authentication.strategy import RedisStrategy
from app.adapter.db.gateway import UserGateway
from app.adapter.permission import UserPermissionCookie
from app.adapter.security import PasswordProvider
from app.application.interfaces import UoW
from app.application.usecase.user import UserUseCase
from app.presentation.interactor import InteractorFactory


class IoC(InteractorFactory):
    def __init__(
            self,
            uow: Annotated[UoW, Dependency(skip_validation=True)],
            user_gateway: UserGateway,
            password_provider: PasswordProvider,
            strategy: RedisStrategy,
    ) -> None:
        self.uow = uow
        self.user_gateway = user_gateway
        self.password_provider = password_provider
        self.strategy = strategy

    @asynccontextmanager
    async def user_usecase(
            self,
            user_permissions: UserPermissionCookie | None = None
    ) -> AsyncIterator[UserUseCase]:
        yield UserUseCase(
            uow=self.uow,
            user_gateway=self.user_gateway,
            password_provider=self.password_provider,
            strategy_redis=self.strategy,
            user_permission=user_permissions
        )
