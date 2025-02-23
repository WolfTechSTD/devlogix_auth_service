from dishka.integrations.base import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import delete, post, status_codes
from litestar.controller import Controller

from app.adapter.exceptions import (
    DecodeError,
    ExpiredSignatureError,
    InvalidPasswordException,
)
from app.application.exceptions import (
    InvalidEmailOrUsername,
    InvalidTokenException,
)
from app.application.interface import IUserPermission
from app.presentation.after_request.cookie import (
    set_access_token_in_cookie,
    set_login_cookie,
    set_logout_cookie,
)
from app.presentation.exception_handlers import forbidden_exception_handler
from app.presentation.exceptions import (
    EmptyTokenException,
    AuthorizedException,
)
from app.presentation.interactor import InteractorFactory
from app.presentation.middleware.auth import (
    CookieUpdatingMiddleware,
    LoginTokenMiddleware,
    LogoutMiddleware,
)
from app.presentation.model.cookie import JsonCookieToken
from app.presentation.model.jwt import (
    JsonAccessToken,
    JsonDeleteRefreshToken,
    JsonRefreshToken,
    JsonToken,
    JsonUpdateAccessToken,
    JsonUpdateRefreshToken,
)
from app.presentation.model.user import JsonUserLogin
from app.presentation.openapi import (
    DeleteRefreshTokenOperation,
    GetTokensOperation,
    LogoutUserOperation,
    UpdateAccessTokenInCookie,
    UpdateAccessTokenOperation,
    UpdateRefreshTokenOperation,
    UserLoginOperation,
)


class AuthController(Controller):
    path = "/api/auth"
    exception_handlers = {
        InvalidPasswordException: forbidden_exception_handler,
        InvalidEmailOrUsername: forbidden_exception_handler,
        InvalidTokenException: forbidden_exception_handler,
        ExpiredSignatureError: forbidden_exception_handler,
        DecodeError: forbidden_exception_handler,
        AuthorizedException: forbidden_exception_handler,
        EmptyTokenException: forbidden_exception_handler,
    }

    @post(
        path="/login",
        operation_class=UserLoginOperation,
        status_code=status_codes.HTTP_200_OK,
        after_request=set_login_cookie,
        middleware=[
            LoginTokenMiddleware,
        ],
    )
    @inject
    async def login(
        self,
        data: JsonUserLogin,
        ioc: Depends[InteractorFactory],
        user_permission: Depends[IUserPermission],
    ) -> JsonCookieToken:
        usecase = ioc.auth_usecase()
        token = await usecase.get_tokens(user_permission, data.into())
        return JsonCookieToken.from_into(
            user_permission.time_access_token,
            user_permission.time_refresh_token,
            token,
        )

    @post(
        path="/jwt",
        operation_class=GetTokensOperation,
        status_code=status_codes.HTTP_201_CREATED,
    )
    @inject
    async def get_tokens(
        self,
        data: JsonUserLogin,
        ioc: Depends[InteractorFactory],
        user_permission: Depends[IUserPermission],
    ) -> JsonToken:
        usecase = ioc.auth_usecase()
        token = await usecase.get_tokens(user_permission, data.into())
        return JsonToken.from_into(token)

    @post(
        "jwt/access",
        operation_class=UpdateAccessTokenOperation,
        status_code=status_codes.HTTP_200_OK,
    )
    @inject
    async def update_access_token(
        self,
        data: JsonUpdateAccessToken,
        ioc: Depends[InteractorFactory],
        user_permission: Depends[IUserPermission],
    ) -> JsonAccessToken:
        usecase = ioc.auth_usecase()
        token = await usecase.update_access_token(user_permission, data.into())
        return JsonAccessToken.from_into(token)

    @post(
        "jwt/refresh",
        operation_class=UpdateRefreshTokenOperation,
        status_code=status_codes.HTTP_200_OK,
    )
    @inject
    async def update_refresh_token(
        self,
        data: JsonUpdateRefreshToken,
        ioc: Depends[InteractorFactory],
        user_permission: Depends[IUserPermission],
    ) -> JsonRefreshToken:
        usecase = ioc.auth_usecase()
        token = await usecase.update_refresh_token(user_permission, data.into())
        return JsonRefreshToken.from_into(token)

    @delete(
        "jwt/delete",
        operation_class=DeleteRefreshTokenOperation,
        status_code=status_codes.HTTP_204_NO_CONTENT,
    )
    @inject
    async def delete_refresh_token(
        self,
        data: JsonDeleteRefreshToken,
        ioc: Depends[InteractorFactory],
    ) -> None:
        usecase = ioc.auth_usecase()
        await usecase.delete_refresh_token(data.into())

    @post(
        "/logout",
        status_code=status_codes.HTTP_204_NO_CONTENT,
        operation_class=LogoutUserOperation,
        after_request=set_logout_cookie,
        middleware=[LogoutMiddleware],
    )
    @inject
    async def logout(
        self,
        data: JsonDeleteRefreshToken,
        ioc: Depends[InteractorFactory],
    ) -> None:
        usecase = ioc.auth_usecase()
        await usecase.delete_refresh_token(data.into())

    @post(
        "/update",
        operation_class=UpdateAccessTokenInCookie,
        status_code=status_codes.HTTP_200_OK,
        after_request=set_access_token_in_cookie,
        middleware=[CookieUpdatingMiddleware],
    )
    @inject
    async def update_access_token_in_cookie(
        self,
        data: JsonUpdateAccessToken,
        ioc: Depends[InteractorFactory],
        user_permission: Depends[IUserPermission],
    ) -> JsonAccessToken:
        usecase = ioc.auth_usecase()
        token = await usecase.update_access_token(user_permission, data.into())
        return JsonAccessToken.from_into(token)
