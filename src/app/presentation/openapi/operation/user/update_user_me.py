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

from app.presentation.openapi.exceptions.base import FORBIDDEN_EXCEPTION
from app.presentation.openapi.exceptions.user import (
    USER_USERNAME_EXISTS,
    USER_EMAIL_EXISTS,
)
from app.presentation.openapi.schema.base import BaseParameters
from app.presentation.openapi.schema.user import UserParameterSchema
from app.presentation.openapi.security.base import BEARER_TOKEN

DESCRIPTION = """
Обновление данных о себе.

* **username** - Юзернейм

* **email** - E-mail

* **password** - Пароль
"""

SUMMARY = "Обновление данных о себе."

REQUEST_BODY_EXAMPLE = {
    "username": "User",
    "email": "user@gmail.com",
    "password": "UserPassword",
}

RESPONSE_EXAMPLE = {
    "id": "01J4HC5WQB3FK3FA1FMXYVYJ6Y",
    "username": "User",
    "email": "user@gmail.com",
    "isActive": True
}


@dataclass
class UpdateUserMeOperation(Operation):
    def __post_init__(self) -> None:
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
                        }
                    ),
                    example=REQUEST_BODY_EXAMPLE
                )
            }
        )
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
