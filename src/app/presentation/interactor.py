from abc import abstractmethod, ABC
from contextlib import AbstractAsyncContextManager

from app.application.interfaces import UserPermission
from app.application.usecase.user import UserUseCase


class InteractorFactory(ABC):
    @abstractmethod
    def user_usecase(
            self,
            user_permissions: UserPermission | None = None
    ) -> AbstractAsyncContextManager[UserUseCase]:
        ...
