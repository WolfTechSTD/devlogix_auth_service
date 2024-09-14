from typing import Annotated

from litestar import (
    Controller,
    post,
    status_codes,
    get,
    Request,
    patch,
    delete,
)
from litestar.params import Dependency, Parameter

from app.adapter.permission import UserPermission
from app.application.interfaces import IUserPermission
from app.application.model.pagination import Pagination
from app.exceptions import (
    UserExistsException,
    UserNotFoundException,
    UserWithUsernameExistsException,
    UserWithEmailExistsException,
    UserLoginException,
    UserWithEmailAndUsernameExistsException,
    InvalidTokenException,
    InvalidAuthenticationTokenError,
    UserAuthException,
)
from app.exceptions.token import TokenTimeException
from app.presentation.after_request.cookie import (
    set_login_cookie,
    set_logout_cookie,
)
from app.presentation.constants import LIMIT, OFFSET
from app.presentation.exception_handlers import (
    bad_request_exception_handler,
    forbidden_exception_handler,
    not_found_exception_handler, unauthorized_exception_handler,
)
from app.presentation.interactor import InteractorFactory
from app.presentation.middleware.token import (
    LoginTokenMiddleware,
    LogoutMiddleware, UserMePermissionMiddleware,
)
from app.presentation.model.cookie import JsonCookieToken
from app.presentation.model.jwt import JsonDeleteRefreshToken
from app.presentation.model.user import (
    JsonCreateUser,
    JsonUser,
    JsonUserLogin, JsonUpdateUserMe, JsonUserList, JsonUpdateUser,
)
from app.presentation.openapi import (
    CreateUserOperation,
    UserLoginOperation,
    LogoutUserOperation,
    GetUserMeOperation,
    UpdateUserMeOperation,
    DeleteUserMeOperation,
    GetUserOperation, GetUsersOperation, UpdateUserOperation,
)

LENGTH_ID = 26


class UserController(Controller):
    path = "/users"
    exception_handlers = {
        UserExistsException: bad_request_exception_handler,
        UserLoginException: forbidden_exception_handler,
        UserNotFoundException: not_found_exception_handler,
        UserWithUsernameExistsException: bad_request_exception_handler,
        UserWithEmailExistsException: bad_request_exception_handler,
        UserWithEmailAndUsernameExistsException: (
            bad_request_exception_handler
        ),
        InvalidAuthenticationTokenError: forbidden_exception_handler,
        InvalidTokenException: forbidden_exception_handler,
        TokenTimeException: unauthorized_exception_handler,
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
        async with ioc.create_user(user_permission) as command:
            user = await command(data.into())
            return JsonUser.from_into(user)

    @post(
        "/login",
        operation_class=UserLoginOperation,
        status_code=status_codes.HTTP_200_OK,
        after_request=set_login_cookie,
        middleware=[LoginTokenMiddleware]
    )
    async def login(
            self,
            data: JsonUserLogin,
            ioc: Annotated[InteractorFactory, Dependency(
                skip_validation=True
            )],
            user_permission: Annotated[UserPermission, Dependency(
                skip_validation=True
            )],
            access_token_time: int,
            refresh_token_time: int
    ) -> JsonCookieToken:
        async with ioc.get_tokens(user_permission) as command:
            token = await command(data.into())
            return JsonCookieToken.from_into(
                access_token_time,
                refresh_token_time,
                token
            )

    @get(
        "/{user_id:str}",
        operation_class=GetUserOperation,
    )
    async def get_user(
            self,
            user_id: Annotated[str, Parameter(
                max_length=LENGTH_ID,
                min_length=LENGTH_ID
            )],
            ioc: Annotated[InteractorFactory, Dependency(
                skip_validation=True
            )],
    ) -> JsonUser:
        async with ioc.get_user() as command:
            user = await command(user_id)
            return JsonUser.from_into(user)

    @get(
        operation_class=GetUsersOperation,
    )
    async def get_users(
            self,
            ioc: Annotated[InteractorFactory, Dependency(
                skip_validation=True
            )],
            limit: int = LIMIT,
            offset: int = OFFSET
    ) -> JsonUserList:
        async with ioc.get_users() as command:
            users = await command(
                Pagination(
                    limit=limit,
                    offset=offset
                )
            )
            return JsonUserList.from_into(limit, offset, users)

    @patch(
        "/{user_id:str}",
        operation_class=UpdateUserOperation,
        status_code=status_codes.HTTP_200_OK,
    )
    async def update_user(
            self,
            user_id: Annotated[str, Parameter(
                max_length=LENGTH_ID,
                min_length=LENGTH_ID
            )],
            data: JsonUpdateUser,
            user_permission: Annotated[UserPermission, Dependency(
                skip_validation=True
            )],
            ioc: Annotated[InteractorFactory, Dependency(skip_validation=True)]
    ) -> JsonUser:
        async with ioc.update_user(user_permission) as command:
            user = await command(data.into(user_id))
            return JsonUser.from_into(user)

    @get(
        "/me",
        operation_class=GetUserMeOperation,
        middleware=[UserMePermissionMiddleware]
    )
    async def get_user_me(
            self,
            request: Request,
            ioc: Annotated[InteractorFactory, Dependency(skip_validation=True)]
    ) -> JsonUser:
        user_id = request.headers.get("user_id")
        async with ioc.get_user_me() as command:
            user = await command(user_id)
            return JsonUser.from_into(user)

    @patch(
        "/me",
        operation_class=UpdateUserMeOperation,
        status_code=status_codes.HTTP_200_OK,
        middleware=[UserMePermissionMiddleware]
    )
    async def update_user_me(
            self,
            data: JsonUpdateUserMe,
            request: Request,
            user_permission: Annotated[UserPermission, Dependency(
                skip_validation=True
            )],
            ioc: Annotated[InteractorFactory, Dependency(skip_validation=True)]
    ) -> JsonUser:
        user_id = request.headers.get("user_id")
        async with ioc.update_user_me(user_permission) as command:
            user = await command(data.into(user_id))
            return JsonUser.from_into(user)

    @delete(
        "/me",
        operation_class=DeleteUserMeOperation,
        status_code=status_codes.HTTP_204_NO_CONTENT,
        after_request=set_logout_cookie,
        middleware=[UserMePermissionMiddleware]
    )
    async def delete_user_me(
            self,
            request: Request,
            ioc: Annotated[InteractorFactory, Dependency(skip_validation=True)]
    ) -> None:
        user_id = request.headers.get("user_id")
        async with ioc.delete_user_me() as command:
            await command(user_id)

    @post(
        "/logout",
        status_code=status_codes.HTTP_204_NO_CONTENT,
        operation_class=LogoutUserOperation,
        after_request=set_logout_cookie,
        middleware=[LogoutMiddleware],
    )
    async def logout(
            self,
            data: JsonDeleteRefreshToken,
            ioc: Annotated[InteractorFactory, Dependency(skip_validation=True)]
    ) -> None:
        async with ioc.delete_refresh_token() as command:
            await command(data.into())
