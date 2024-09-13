from typing import Annotated

from litestar import post, status_codes, delete
from litestar.controller import Controller
from litestar.params import Dependency

from app.application.interfaces import IUserPermission
from app.exceptions import (
    UserLoginException,
    InvalidTokenException,
)
from app.presentation.exception_handlers import forbidden_exception_handler
from app.presentation.interactor import InteractorFactory
from app.presentation.model.jwt import (
    JsonToken,
    JsonUpdateAccessToken,
    JsonAccessToken,
    JsonUpdateRefreshToken,
    JsonRefreshToken,
    JsonDeleteRefreshToken,
)
from app.presentation.model.user import JsonUserLogin
from app.presentation.openapi import (
    GetTokensOperation,
    UpdateAccessTokenOperation,
    UpdateRefreshTokenOperation,
    DeleteRefreshTokenOperation,
)


class JWTController(Controller):
    path = "/jwt"
    exception_handlers = {
        UserLoginException: forbidden_exception_handler,
        InvalidTokenException: forbidden_exception_handler
    }

    @post(
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
        async with ioc.get_tokens(user_permission) as command:
            token = await command(data.into())
            return JsonToken.from_into(token)

    @post(
        "/access",
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
        async with ioc.update_access_token(user_permission) as command:
            token = await command(data.into())
            return JsonAccessToken.from_into(token)

    @post(
        "/refresh",
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
        async with ioc.update_refresh_token(user_permission) as command:
            token = await command(data.into())
            return JsonRefreshToken.from_into(token)

    @delete(
        "/delete",
        operation_class=DeleteRefreshTokenOperation,
        status_code=status_codes.HTTP_204_NO_CONTENT
    )
    async def delete_refresh_token(
            self,
            data: JsonDeleteRefreshToken,
            ioc: Annotated[InteractorFactory, Dependency(skip_validation=True)]
    ) -> None:
        async with ioc.delete_refresh_token() as command:
            await command(data.into())
