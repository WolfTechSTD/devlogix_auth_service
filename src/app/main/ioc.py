from collections.abc import Iterator
from contextlib import contextmanager

from app.adapter.repository.user import UserRepository
from app.application.usecase.user import UserUseCase
from app.presentation.interactor import InteractorFactory


class IoC(InteractorFactory):
    def __init__(
            self,
            user_repository: UserRepository
    ) -> None:
        self.user_repository = user_repository

    @contextmanager
    def add_user_usecase(self) -> Iterator[UserUseCase]:
        yield UserUseCase(
            repository=self.user_repository
        )
