from typing import Annotated

from litestar import (
    Controller,
    post,
    status_codes,
    get,
    Request, patch, delete,
)
from litestar.params import Dependency, Parameter

from app.adapter.exceptions import InvalidAuthenticationTokenError

from app.application.exceptions import (
    UserExistsException,
    UserNotFoundException,
    UserWithUsernameExistsException,
    UserWithEmailExistsException,
    UserLoginException,
    UserWithEmailAndUsernameExistsException,
    InvalidTokenException,
)
from app.application.interfaces import UserPermissionCookie
from app.presentation.after_request.token import set_login_cookie
from app.presentation.constants import LIMIT, OFFSET

from app.presentation.exception_handlers import (
    user_bad_request_exception_handler,
    user_forbidden_exception_handler,
    user_not_found_exception_handler,
)

from app.presentation.interactor import InteractorFactory
from app.presentation.middleware.token import (
    LoginCookieTokenMiddleware,
    CookieTokenPermissionMiddleware,
)
from app.presentation.model.token import JsonCookieToken
from app.presentation.model.user import (
    JsonCreateUser,
    JsonUser,
    JsonUserLogin, JsonUserList, JsonUpdateUser, JsonUpdateUserMe,
)
from app.presentation.openapi import (
    CreateUserOperation,
    UserLoginOperation,
    GetUserOperation,
    GetUsersOperation,
    UpdateUserOperation,
    GetUserMeOperation, UpdateUserMeOperation, DeleteUserMeOperation,
)

LENGTH_ID = 26


class UserController(Controller):
    path = "/users"
    exception_handlers = {
        UserExistsException: user_bad_request_exception_handler,
        UserLoginException: user_forbidden_exception_handler,
        UserNotFoundException: user_not_found_exception_handler,
        UserWithUsernameExistsException: user_bad_request_exception_handler,
        UserWithEmailExistsException: user_bad_request_exception_handler,
        UserWithEmailAndUsernameExistsException: (
            user_bad_request_exception_handler
        ),
        InvalidAuthenticationTokenError: user_forbidden_exception_handler,
        InvalidTokenException: user_forbidden_exception_handler,
    }

    @post(
        operation_class=CreateUserOperation,
        status_code=status_codes.HTTP_201_CREATED
    )
    async def create_user(
            self,
            data: JsonCreateUser,
            ioc: Annotated[InteractorFactory, Dependency(skip_validation=True)]
    ) -> JsonUser:
        async with ioc.user_usecase() as use_case:
            user = await use_case.create_user(data.into())
            return JsonUser.from_into(user)

    @post(
        "/login",
        operation_class=UserLoginOperation,
        status_code=status_codes.HTTP_200_OK,
        after_request=set_login_cookie,
        middleware=[LoginCookieTokenMiddleware]
    )
    async def login(
            self,
            data: JsonUserLogin,
            ioc: Annotated[InteractorFactory, Dependency(skip_validation=True)]
    ) -> JsonCookieToken:
        async with ioc.user_usecase() as user_use_case:
            cookie = await user_use_case.login(data.into())
            return JsonCookieToken.from_into(cookie)

    @get(
        "/{user_id:str}",
        operation_class=GetUserOperation,
        middleware=[CookieTokenPermissionMiddleware]
    )
    async def get_user(
            self,
            request: Request,
            user_id: Annotated[str, Parameter(
                max_length=LENGTH_ID,
                min_length=LENGTH_ID
            )],
            ioc: Annotated[InteractorFactory, Dependency(
                skip_validation=True
            )],
            user_permissions: Annotated[UserPermissionCookie, Dependency(
                skip_validation=True
            )],
    ) -> JsonUser:
        token = request.cookies.get("session")
        async with ioc.user_usecase(user_permissions) as user_use_case:
            user = await user_use_case.get_user(user_id, token)
            return JsonUser.from_into(user)

    @get(
        operation_class=GetUsersOperation,
        middleware=[CookieTokenPermissionMiddleware]
    )
    async def get_users(
            self,
            request: Request,
            ioc: Annotated[InteractorFactory, Dependency(
                skip_validation=True
            )],
            user_permissions: Annotated[UserPermissionCookie, Dependency(
                skip_validation=True
            )],
            limit: int = LIMIT,
            offset: int = OFFSET
    ) -> JsonUserList:
        token = request.cookies.get("session")
        async with ioc.user_usecase(user_permissions) as user_use_case:
            users = await user_use_case.get_users(limit, offset, token)
            return JsonUserList.from_into(limit, offset, users)

    @patch(
        "/{user_id:str}",
        operation_class=UpdateUserOperation,
        status_code=status_codes.HTTP_200_OK,
        middleware=[CookieTokenPermissionMiddleware]
    )
    async def update_user(
            self,
            request: Request,
            user_id: Annotated[str, Parameter(
                max_length=LENGTH_ID,
                min_length=LENGTH_ID
            )],
            data: JsonUpdateUser,
            user_permissions: Annotated[UserPermissionCookie, Dependency(
                skip_validation=True
            )],
            ioc: Annotated[InteractorFactory, Dependency(skip_validation=True)]
    ) -> JsonUser:
        token = request.cookies.get("session")
        async with ioc.user_usecase(user_permissions) as user_use_case:
            user = await user_use_case.update_user(data.into(user_id), token)
            return JsonUser.from_into(user)

    @get(
        "/me",
        operation_class=GetUserMeOperation,
        middleware=[CookieTokenPermissionMiddleware]
    )
    async def get_user_me(
            self,
            request: Request,
            user_permissions: Annotated[UserPermissionCookie, Dependency(
                skip_validation=True
            )],
            ioc: Annotated[InteractorFactory, Dependency(skip_validation=True)]
    ) -> JsonUser:
        token = request.cookies.get("session")
        async with ioc.user_usecase(user_permissions) as user_use_case:
            user = await user_use_case.get_user_me(token)
            return JsonUser.from_into(user)

    @patch(
        "/me",
        operation_class=UpdateUserMeOperation,
        status_code=status_codes.HTTP_200_OK,
        middleware=[CookieTokenPermissionMiddleware]
    )
    async def update_user_me(
            self,
            data: JsonUpdateUserMe,
            request: Request,
            user_permissions: Annotated[UserPermissionCookie, Dependency(
                skip_validation=True
            )],
            ioc: Annotated[InteractorFactory, Dependency(skip_validation=True)]
    ) -> JsonUser:
        token = request.cookies.get("session")
        async with ioc.user_usecase(user_permissions) as user_use_case:
            user = await user_use_case.update_user_me(data.into(), token)
            return JsonUser.from_into(user)

    @delete(
        "/me",
        operation_class=DeleteUserMeOperation,
        status_code=status_codes.HTTP_204_NO_CONTENT,
        middleware=[CookieTokenPermissionMiddleware]
    )
    async def delete_user_me(
            self,
            request: Request,
            user_permissions: Annotated[UserPermissionCookie, Dependency(
                skip_validation=True
            )],
            ioc: Annotated[InteractorFactory, Dependency(skip_validation=True)]
    ) -> None:
        token = request.cookies.get("session")
        async with ioc.user_usecase(user_permissions) as user_use_case:
            await user_use_case.delete_user_me(token)
