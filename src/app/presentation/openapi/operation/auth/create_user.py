from dataclasses import dataclass

from litestar.openapi.spec import (
    OpenAPIMediaType,
    Operation,
    RequestBody,
    Schema,
    OpenAPIResponse,
    OpenAPIType,
)

from app.presentation.openapi.schema.base import BaseParameters
from app.presentation.openapi.exceptions.base import (
    FORBIDDEN_EXCEPTION,
)
from app.presentation.openapi.exceptions.user import USER_EXISTS_EXCEPTION
from app.presentation.openapi.schema.user import UserParameterSchema

DESCRIPTION = """
Создание пользователя.

* **username** - Юзернейм

* **email** - E-mail

* **password** - Пароль
"""

SUMMARY = "Создание пользователя"

REQUEST_BODY_EXAMPLE = {
    "username": "User",
    "email": "user@gmail.com",
    "password": "UserPassword"
}

RESPONSE_EXAMPLE = {
    "id": "01J4HC5WQB3FK3FA1FMXYVYJ6Y",
    "username": "User",
    "email": "user@gmail.com",
    "isActive": True
}


@dataclass
class CreateUserOperation(Operation):
    def __post_init__(self) -> None:
        self.tags = ["auth"]
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
                        required=("username", "email", "password")
                    ),
                    example=REQUEST_BODY_EXAMPLE,
                )
            }
        )
        self.responses = {
            "201": OpenAPIResponse(
                description="Created",
                content={
                    "json": OpenAPIMediaType(
                        schema=Schema(
                            type=OpenAPIType.OBJECT,
                            properties={
                                "id": UserParameterSchema.id,
                                "username": UserParameterSchema.username,
                                "email": UserParameterSchema.email,
                                "isActive": UserParameterSchema.is_active
                            }
                        ),
                        example=RESPONSE_EXAMPLE
                    )
                }
            ),
            "400": OpenAPIResponse(
                description="Bad Request",
                content={
                    "json": OpenAPIMediaType(
                        schema=Schema(
                            type=OpenAPIType.OBJECT,
                            properties={
                                "status_code": BaseParameters.status_code,
                                "detail": BaseParameters.detail
                            }
                        ),
                        example=USER_EXISTS_EXCEPTION
                    )
                }
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
                        example=FORBIDDEN_EXCEPTION
                    )
                }
            )
        }
