from typing import Annotated

from litestar import Controller, post, status_codes, get, patch
from litestar.exceptions import HTTPException
from litestar.params import Dependency, Parameter

from app.application.exceptions import (
    UserExistsException,
    UserNotFoundException,
    UserWithUsernameExistsException,
    UserWithEmailExistsException, UserLoginException,
)
from app.presentation.interactor import InteractorFactory
from app.presentation.model.user import (
    JsonCreateUser,
    JsonUser,
    JsonUserList,
    JsonUpdateUser, JsonUserLogin,
)
from app.presentation.openapi.user.create_user import CreateUserOperation
from app.presentation.openapi.user.get_user import GetUserOperation
from app.presentation.openapi.user.get_users import GetUsersOperation
from app.presentation.openapi.user.login import UserLoginOperation
from app.presentation.openapi.user.update_user import UpdateUserOperation

LENGTH_ID = 26


class UserController(Controller):
    path = "/users"

    @post(
        operation_class=CreateUserOperation,
        status_code=status_codes.HTTP_201_CREATED
    )
    async def create_user(
            self,
            data: JsonCreateUser,
            ioc: Annotated[InteractorFactory, Dependency(skip_validation=True)]
    ) -> JsonUser:
        try:
            with ioc.add_user_usecase() as user_use_case:
                user = await user_use_case.create_user(data.into())
                return JsonUser.from_into(user)
        except UserExistsException as err:
            raise HTTPException(
                status_code=status_codes.HTTP_400_BAD_REQUEST,
                detail=str(err)
            )

    @post(
        "/login",
        operation_class=UserLoginOperation
    )
    async def login(
            self,
            data: JsonUserLogin,
            ioc: Annotated[InteractorFactory, Dependency(skip_validation=True)]
    ) -> JsonUser:
        try:
            with ioc.add_user_usecase() as user_use_case:
                user = await user_use_case.login(data.into())
                return JsonUser.from_into(user)
        except UserLoginException as err:
            raise HTTPException(
                status_code=status_codes.HTTP_403_FORBIDDEN,
                detail=str(err)
            )

    @get(
        "/{user_id:str}",
        operation_class=GetUserOperation
    )
    async def get_user(
            self,
            user_id: Annotated[str, Parameter(
                max_length=LENGTH_ID,
                min_length=LENGTH_ID
            )],
            ioc: Annotated[InteractorFactory, Dependency(skip_validation=True)]
    ) -> JsonUser:
        try:
            with ioc.add_user_usecase() as user_use_case:
                user = await user_use_case.get_user(user_id)
                return JsonUser.from_into(user)
        except UserNotFoundException as err:
            raise HTTPException(
                status_code=status_codes.HTTP_404_NOT_FOUND,
                detail=str(err)
            )

    @get(operation_class=GetUsersOperation)
    async def get_users(
            self,
            ioc: Annotated[InteractorFactory, Dependency(
                skip_validation=True
            )],
            limit: int = 10,
            offset: int = 0
    ) -> JsonUserList:
        with ioc.add_user_usecase() as user_use_case:
            users = await user_use_case.get_users(limit, offset)
            return JsonUserList.from_into(limit, offset, users)

    @patch(
        "/{user_id:str}",
        operation_class=UpdateUserOperation,
    )
    async def update_user(
            self,
            user_id: Annotated[str, Parameter(
                max_length=LENGTH_ID,
                min_length=LENGTH_ID
            )],
            data: JsonUpdateUser,
            ioc: Annotated[InteractorFactory, Dependency(skip_validation=True)]
    ) -> JsonUser:
        try:
            with ioc.add_user_usecase() as user_use_case:
                user = await user_use_case.update_user(data.into(user_id))
                return JsonUser.from_into(user)
        except UserNotFoundException as err:
            raise HTTPException(
                status_code=status_codes.HTTP_404_NOT_FOUND,
                detail=str(err)
            )
        except (UserWithUsernameExistsException,
                UserWithEmailExistsException) as err:
            raise HTTPException(
                status_code=status_codes.HTTP_400_BAD_REQUEST,
                detail=str(err)
            )
