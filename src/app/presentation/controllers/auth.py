from typing import Annotated

from litestar import post, status_codes, delete
from litestar.controller import Controller
from litestar.params import Dependency

from app.application.interfaces import IUserPermission
from app.exceptions import (
    UserLoginException,
    InvalidTokenException,
    UserAuthException,
)
from app.presentation.after_request.cookie import (
    set_login_cookie,
    set_logout_cookie, set_access_token,
)
from app.presentation.exception_handlers import (
    forbidden_exception_handler,
    bad_request_exception_handler,
)
from app.presentation.interactor import InteractorFactory
from app.presentation.middleware.auth import (
    LoginTokenMiddleware,
    LogoutMiddleware, CookieUpdatingMiddleware,
)
from app.presentation.model.cookie import JsonCookieToken
from app.presentation.model.jwt import (
    JsonToken,
    JsonUpdateAccessToken,
    JsonAccessToken,
    JsonUpdateRefreshToken,
    JsonRefreshToken,
    JsonDeleteRefreshToken,
)
from app.presentation.model.user import JsonUserLogin, JsonCreateUser, JsonUser
from app.presentation.openapi import (
    GetTokensOperation,
    UpdateAccessTokenOperation,
    UpdateRefreshTokenOperation,
    DeleteRefreshTokenOperation,
    UserLoginOperation,
    LogoutUserOperation,
    CreateUserOperation, UpdateAccessTokenInCookie,
)


class AuthController(Controller):
    path = "/api/auth"
    exception_handlers = {
        UserLoginException: forbidden_exception_handler,
        InvalidTokenException: forbidden_exception_handler,
        UserAuthException: bad_request_exception_handler
    }

    @post(
        operation_class=CreateUserOperation,
        status_code=status_codes.HTTP_201_CREATED
    )
    async def create_user(
            self,
            data: JsonCreateUser,
            ioc: Annotated[InteractorFactory, Dependency(
                skip_validation=True
            )],
            user_permission: Annotated[IUserPermission, Dependency(
                skip_validation=True
            )],
    ) -> JsonUser:
        async with ioc.auth_usecase() as auth:
            user = await auth.create_user(user_permission, data.into())
            return JsonUser.from_into(user)

    @post(
        path="/login",
        operation_class=UserLoginOperation,
        status_code=status_codes.HTTP_200_OK,
        after_request=set_login_cookie,
        middleware=[LoginTokenMiddleware, ]
    )
    async def login(
            self,
            data: JsonUserLogin,
            ioc: Annotated[InteractorFactory, Dependency(
                skip_validation=True
            )],
            user_permission: Annotated[IUserPermission, Dependency(
                skip_validation=True
            )],
            access_token_time: int,
            refresh_token_time: int,
    ) -> JsonCookieToken:
        async with ioc.auth_usecase() as auth:
            token = await auth.get_tokens(user_permission, data.into())
            return JsonCookieToken.from_into(
                access_token_time,
                refresh_token_time,
                token,
            )

    @post(
        path="/jwt",
        operation_class=GetTokensOperation,
        status_code=status_codes.HTTP_201_CREATED
    )
    async def get_tokens(
            self,
            data: JsonUserLogin,
            ioc: Annotated[InteractorFactory, Dependency(
                skip_validation=True
            )],
            user_permission: Annotated[IUserPermission, Dependency(
                skip_validation=True
            )],
    ) -> JsonToken:
        async with ioc.auth_usecase() as auth:
            token = await auth.get_tokens(user_permission, data.into())
            return JsonToken.from_into(token)

    @post(
        "jwt/access",
        operation_class=UpdateAccessTokenOperation,
        status_code=status_codes.HTTP_200_OK
    )
    async def update_access_token(
            self,
            data: JsonUpdateAccessToken,
            ioc: Annotated[InteractorFactory, Dependency(
                skip_validation=True
            )],
            user_permission: Annotated[IUserPermission, Dependency(
                skip_validation=True
            )],
    ) -> JsonAccessToken:
        async with ioc.auth_usecase() as auth:
            token = await auth.update_access_token(
                user_permission,
                data.into()
            )
            return JsonAccessToken.from_into(token)

    @post(
        "jwt/refresh",
        operation_class=UpdateRefreshTokenOperation,
        status_code=status_codes.HTTP_200_OK
    )
    async def update_refresh_token(
            self,
            data: JsonUpdateRefreshToken,
            ioc: Annotated[InteractorFactory, Dependency(
                skip_validation=True
            )],
            user_permission: Annotated[IUserPermission, Dependency(
                skip_validation=True
            )],
    ) -> JsonRefreshToken:
        async with ioc.auth_usecase() as auth:
            token = await auth.update_refresh_token(
                user_permission,
                data.into()
            )
            return JsonRefreshToken.from_into(token)

    @delete(
        "jwt/delete",
        operation_class=DeleteRefreshTokenOperation,
        status_code=status_codes.HTTP_204_NO_CONTENT
    )
    async def delete_refresh_token(
            self,
            data: JsonDeleteRefreshToken,
            ioc: Annotated[InteractorFactory, Dependency(skip_validation=True)]
    ) -> None:
        async with ioc.auth_usecase() as auth:
            await auth.delete_refresh_token(data.into())

    @post(
        "/logout",
        status_code=status_codes.HTTP_204_NO_CONTENT,
        operation_class=LogoutUserOperation,
        after_request=set_logout_cookie,
        middleware=[LogoutMiddleware]
    )
    async def logout(
            self,
            data: JsonDeleteRefreshToken,
            ioc: Annotated[InteractorFactory, Dependency(skip_validation=True)]
    ) -> None:
        async with ioc.auth_usecase() as auth:
            await auth.delete_refresh_token(data.into())

    @post(
        "/update",
        operation_class=UpdateAccessTokenInCookie,
        status_code=status_codes.HTTP_200_OK,
        after_request=set_access_token,
        middleware=[CookieUpdatingMiddleware]
    )
    async def update_access_token_in_cookie(
            self,
            data: JsonUpdateAccessToken,
            ioc: Annotated[InteractorFactory, Dependency(
                skip_validation=True
            )],
            user_permission: Annotated[IUserPermission, Dependency(
                skip_validation=True
            )],
    ) -> JsonAccessToken:
        async with ioc.auth_usecase() as auth:
            token = await auth.update_access_token(
                user_permission,
                data.into()
            )
            return JsonAccessToken.from_into(token)
