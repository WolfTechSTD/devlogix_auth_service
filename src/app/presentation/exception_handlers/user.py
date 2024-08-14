from typing import Union

from litestar import Request, Response, status_codes

from app.adapter.exceptions.permissions import InvalidCookieTokenException
from app.application.exceptions import (
    UserExistsException,
    UserLoginException,
    UserNotFoundException,
    UserWithUsernameExistsException,
    UserWithEmailExistsException,
    UserWithEmailAndUsernameExistsException, InvalidTokenException,
)


def user_bad_request_exception_handler(
        _: Request,
        exc: Union[
            UserExistsException,
            UserWithUsernameExistsException,
            UserWithEmailExistsException,
            UserWithEmailAndUsernameExistsException
        ]
) -> Response:
    return Response(
        content={
            "status_code": status_codes.HTTP_400_BAD_REQUEST,
            "detail": str(exc)
        },
        status_code=status_codes.HTTP_400_BAD_REQUEST
    )


def user_forbidden_exception_handler(
        _: Request,
        exc: Union[
            UserLoginException,
            InvalidCookieTokenException,
            InvalidTokenException
        ]
) -> Response:
    return Response(
        content={
            "status_code": status_codes.HTTP_403_FORBIDDEN,
            "detail": str(exc)
        },
        status_code=status_codes.HTTP_403_FORBIDDEN
    )


def user_not_found_exception_handler(
        _: Request,
        exc: UserNotFoundException
) -> Response:
    return Response(
        content={
            "status_code": status_codes.HTTP_404_NOT_FOUND,
            "detail": str(exc)
        },
        status_code=status_codes.HTTP_404_NOT_FOUND
    )
