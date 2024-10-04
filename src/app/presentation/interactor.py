from abc import abstractmethod, ABC
from contextlib import AbstractAsyncContextManager

from app.application.interfaces import IUserPermission
from app.application.usecase.auth import (
    GetTokens,
    UpdateAccessToken,
    UpdateRefreshToken,
    DeleteRefreshToken,
    CreateUser,
)


class InteractorFactory(ABC):
    @abstractmethod
    def create_user(
            self,
            user_permission: IUserPermission
    ) -> AbstractAsyncContextManager[CreateUser]: ...

    @abstractmethod
    def get_tokens(
            self,
            user_permission: IUserPermission
    ) -> AbstractAsyncContextManager[GetTokens]: ...

    @abstractmethod
    def update_access_token(
            self,
            user_permission: IUserPermission
    ) -> AbstractAsyncContextManager[UpdateAccessToken]: ...

    @abstractmethod
    def update_refresh_token(
            self,
            user_permission: IUserPermission
    ) -> AbstractAsyncContextManager[UpdateRefreshToken]: ...

    @abstractmethod
    def delete_refresh_token(
            self
    ) -> AbstractAsyncContextManager[DeleteRefreshToken]: ...
