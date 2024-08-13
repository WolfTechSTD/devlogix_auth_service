from dataclasses import dataclass

from litestar.openapi.spec import (
    OpenAPIMediaType,
    Operation,
    RequestBody,
    Schema,
    OpenAPIResponse,
    OpenAPIType,
    Example,
)

from app.presentation.openapi.base import BaseParameters
from app.presentation.openapi.exceptions.base import INVALID_DATA_EXCEPTION
from app.presentation.openapi.user.schema import UserParameterSchema

DESCRIPTION = """
Аутентификация

* **username** - юзернейм

* **email** - e-mail

* **password** - пароль
"""

SUMMARY = "Аутентификация"

REQUEST_BODY_USERNAME_EXAMPLE = {
    "username": "User",
    "password": "UserPassword"
}

REQUEST_BODY_EMAIL_EXAMPLE = {
    "email": "user@gmail.com",
    "password": "UserPassword"
}


@dataclass
class UserLoginOperation(Operation):
    def __post_init__(self) -> None:
        self.tags = ["users"]
        self.summary = SUMMARY
        self.description = DESCRIPTION
        self.request_body = RequestBody(
            content={
                "json": OpenAPIMediaType(
                    schema=Schema(
                        type=OpenAPIType.OBJECT,
                        properties={
                            "username": UserParameterSchema.username,
                            "email": UserParameterSchema.email,
                            "password": UserParameterSchema.password
                        },
                        required=("password",)
                    ),
                    examples={
                        "Ввода с юзернеймом": Example(
                            value=REQUEST_BODY_USERNAME_EXAMPLE
                        ),
                        "Ввод с e-mail": Example(
                            value=REQUEST_BODY_EMAIL_EXAMPLE
                        )
                    }
                )
            }
        )
        self.responses = {
            "200": OpenAPIResponse(
                description="Ok",
                content=None
            ),
            "403": OpenAPIResponse(
                description="Forbidden",
                content={
                    "json": OpenAPIMediaType(
                        schema=Schema(
                            type=OpenAPIType.OBJECT,
                            properties={
                                "status_code": BaseParameters.status_code,
                                "detail": BaseParameters.detail
                            }
                        ),
                        example=INVALID_DATA_EXCEPTION
                    )
                }
            )
        }
