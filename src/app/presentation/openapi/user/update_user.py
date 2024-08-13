from dataclasses import dataclass

from litestar.openapi.spec import (
    OpenAPIMediaType,
    Operation,
    RequestBody,
    Schema,
    OpenAPIResponse,
    OpenAPIType,
    Example,
    Parameter,
)

from app.presentation.openapi.base import BaseParameters
from app.presentation.openapi.exceptions.base import FORBIDDEN_EXCEPTION
from app.presentation.openapi.exceptions.user import (
    USER_EMAIL_EXISTS,
    USER_USERNAME_EXISTS, USER_NOT_FOUND_EXCEPTION,
)
from app.presentation.openapi.security.base import BEARER_TOKEN
from app.presentation.openapi.user.schema import UserParameterSchema

DESCRIPTION = """
Обновление пользователя.

* **username** - Юзернейм

* **email** - E-mail

* **password** - Пароль

* **isActive** - Статус пользователя
"""

SUMMARY = "Обновление пользователя"

REQUEST_BODY_EXAMPLE = {
    "username": "User",
    "email": "user@gmail.com",
    "password": "UserPassword",
    "isActive": True
}

RESPONSE_EXAMPLE = {
    "id": "01J4HC5WQB3FK3FA1FMXYVYJ6Y",
    "username": "User",
    "email": "user@gmail.com",
    "isActive": True
}


@dataclass
class UpdateUserOperation(Operation):
    def __post_init__(self):
        self.tags = ["users"]
        self.summary = SUMMARY
        self.description = DESCRIPTION
        self.security = [BEARER_TOKEN]
        self.request_body = RequestBody(
            content={
                "json": OpenAPIMediaType(
                    schema=Schema(
                        type=OpenAPIType.OBJECT,
                        properties={
                            "username": UserParameterSchema.username,
                            "email": UserParameterSchema.email,
                            "password": UserParameterSchema.password,
                            "isActive": UserParameterSchema.is_active
                        }
                    ),
                    example=REQUEST_BODY_EXAMPLE
                )
            }
        )
        self.parameters = [Parameter(
            name="user_id",
            param_in="path",
            required=True,
            schema=UserParameterSchema.user_id
        )]
        self.responses = {
            "200": OpenAPIResponse(
                description="Ok",
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
                        examples={
                            "Пользователь не найден": Example(
                                value=USER_NOT_FOUND_EXCEPTION
                            ),
                            "Пользователь с юзернейм уже существует": Example(
                                value=USER_USERNAME_EXISTS
                            ),
                            "Пользователь с почтой уже существует": Example(
                                value=USER_EMAIL_EXISTS
                            )
                        }
                    )
                }
            ),
            "403": OpenAPIResponse(
                description="Not Found",
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
