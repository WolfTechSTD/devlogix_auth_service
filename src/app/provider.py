from typing import AsyncIterator

from dishka import Provider, from_context, Scope, provide, AnyOf
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.adapter.permission import UserPermission
from app.adapter.persistence import new_session_maker
from app.adapter.security import PasswordProvider, TokenProvider
from app.application.interface import (
    IUserPermission,
    ITokenProvider,
    IPasswordProvider,
)
from app.config import ApplicationConfig, JWTConfig
from app.ioc import IoC
from app.presentation.interactor import InteractorFactory


class AppProvider(Provider):
    config = from_context(
        provides=ApplicationConfig,
        scope=Scope.APP
    )

    @provide(scope=Scope.APP)
    def get_session_maker(
            self,
            config: ApplicationConfig
    ) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.db)

    @provide(scope=Scope.APP)
    def get_jwt_config(self, config: ApplicationConfig) -> JWTConfig:
        return config.jwt

    @provide(scope=Scope.REQUEST)
    async def get_session(
            self,
            session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterator[AsyncSession]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.APP)
    def get_password_provider(
            self
    ) -> AnyOf[PasswordProvider, IPasswordProvider]:
        return PasswordProvider()

    @provide(scope=Scope.APP)
    def get_jwt_provider(
            self,
            jwt_config: JWTConfig
    ) -> AnyOf[TokenProvider, ITokenProvider]:
        return TokenProvider(
            config=jwt_config
        )

    ioc = provide(
        IoC,
        scope=Scope.REQUEST,
        provides=AnyOf[InteractorFactory]
    )
    user_permission = provide(
        UserPermission,
        scope=Scope.REQUEST,
        provides=AnyOf[IUserPermission]
    )
