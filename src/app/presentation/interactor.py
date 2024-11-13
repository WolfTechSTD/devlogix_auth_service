from abc import abstractmethod, ABC
from contextlib import AbstractAsyncContextManager

from app.application.usecase.auth import AuthUseCase
from app.application.usecase.user import UserUseCase


class InteractorFactory(ABC):
    @abstractmethod
    def auth_usecase(self) -> AuthUseCase: ...

    @abstractmethod
    def user_usecase(self) -> UserUseCase: ...
