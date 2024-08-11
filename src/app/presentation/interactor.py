from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager

from app.application.usecase.user import UserUseCase


class InteractorFactory(ABC):
    @abstractmethod
    def add_user_usecase(self) -> AbstractAsyncContextManager[UserUseCase]: ...
