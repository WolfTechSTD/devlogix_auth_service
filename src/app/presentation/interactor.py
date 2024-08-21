from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager

from app.application.usecase.user import UserUseCase
from app.kernel.permissions.user import UserPermissions


class InteractorFactory(ABC):
    @abstractmethod
    def user_usecase(
            self,
            user_permissions: UserPermissions | None = None
    ) -> AbstractAsyncContextManager[UserUseCase]:
        ...
