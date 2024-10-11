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

from app.presentation.openapi.exceptions.base import INVALID_DATA_EXCEPTION
from app.presentation.openapi.schema.base import BaseParameters
from app.presentation.openapi.schema.jwt import JWTParameterSchema
from app.presentation.openapi.schema.user import UserParameterSchema

DESCRIPTION = """
Получение токенов.

* **username** - Юзернейм

* **email** - E-mail

* **password** - Пароль
"""

SUMMARY = "Получение токенов"

REQUEST_BODY_USERNAME_EXAMPLE = {
    "username": "User",
    "password": "UserPassword"
}

REQUEST_BODY_EMAIL_EXAMPLE = {
    "email": "user@gmail.com",
    "password": "UserPassword"
}

RESPONSE_EXAMPLE = {
    "tokenType": "Bearer",
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
                   "eyJpZCI6IjAxSjVXWDNXVkNGTVhFWVc1NEoxUFlDSFJL"
                   "IiwiZGF0ZV9vbiI6IjIwMjQtMDgtMjQgMTc6Mjk6MzYuNTk"
                   "3MDM5KzAwOjAwIiwiZXhwIjoxNzI0NTIxNDc2fQ.qRUrXC"
                   "xuC99sljk7k4O-ElYsDGk7ck3DHkAfirdZC7E",
    "expiresIn": 900,
    "refreshToken": "f4Xzh6M4syUf6jZPZizF0FFlC4vuO2HHLHj3GiZHDok"
}


@dataclass
class GetTokensOperation(Operation):
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
            "201": OpenAPIResponse(
                description="Created",
                content={
                    "json": OpenAPIMediaType(
                        schema=Schema(
                            type=OpenAPIType.OBJECT,
                            properties={
                                "tokenType": JWTParameterSchema.token_type,
                                "accessToken": JWTParameterSchema.access_token,
                                "expiresIn": JWTParameterSchema.expire_in,
                                "refreshToken": JWTParameterSchema.refresh_token,
                            }
                        ),
                        example=RESPONSE_EXAMPLE
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
                        example=INVALID_DATA_EXCEPTION
                    )
                }
            )
        }
