from abc import abstractmethod, ABC
from contextlib import AbstractAsyncContextManager

from app.application.interfaces import IUserPermission
from app.application.usecase.jwt.delete_refresh_token import DeleteRefreshToken
from app.application.usecase.jwt.get_tokens import GetTokens
from app.application.usecase.jwt.update_accesss_token import UpdateAccessToken
from app.application.usecase.jwt.update_refresh_token import UpdateRefreshToken
from app.application.usecase.user.create_user import CreateUser
from app.application.usecase.user.delete_user_me import DeleteUserMe
from app.application.usecase.user.get_user_me import GetUserMe
from app.application.usecase.user.update_user_me import UpdateUserMe


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

    @abstractmethod
    def get_user_me(self) -> AbstractAsyncContextManager[GetUserMe]: ...

    @abstractmethod
    def update_user_me(
            self,
            user_permission: IUserPermission
    ) -> AbstractAsyncContextManager[UpdateUserMe]: ...

    @abstractmethod
    def delete_user_me(self) -> AbstractAsyncContextManager[DeleteUserMe]: ...
