from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from app.adapter.repository.cookie_token import CookieTokenRepository
from app.adapter.repository.user import UserRepository
from app.adapter.security.password import PasswordProvider
from app.application.usecase.user import UserUseCase
from app.presentation.interactor import InteractorFactory


class IoC(InteractorFactory):
    def __init__(
            self,
            user_repository: UserRepository,
            password_provider: PasswordProvider,
            cookie_token_repository: CookieTokenRepository
    ) -> None:
        self.user_repository = user_repository
        self.password_provider = password_provider
        self.cookie_token_repository = cookie_token_repository

    @asynccontextmanager
    async def add_user_usecase(self) -> AsyncIterator[UserUseCase]:
        yield UserUseCase(
            repository=self.user_repository,
            password_provider=self.password_provider,
            cookie_token_repository=self.cookie_token_repository
        )
