from abc import abstractmethod, ABC
from contextlib import AbstractAsyncContextManager

from app.application.usecase.auth import AuthUseCase


class InteractorFactory(ABC):
    @abstractmethod
    def auth_usecase(self) -> AbstractAsyncContextManager[AuthUseCase]: ...
