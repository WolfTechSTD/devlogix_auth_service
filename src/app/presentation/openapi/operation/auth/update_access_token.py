from dataclasses import dataclass

from litestar.openapi.spec import (
    Operation,
    RequestBody,
    OpenAPIMediaType,
    Schema,
    OpenAPIType,
    OpenAPIResponse,
)

from app.presentation.openapi.exceptions.base import FORBIDDEN_EXCEPTION
from app.presentation.openapi.schema.base import BaseParameters
from app.presentation.openapi.schema.jwt import JWTParameterSchema

DESCRIPTION = """
Обновление токена доступа.

* **refreshToken** - Токен обновления
"""

SUMMARY = "Обновление токена доступа"

REQUEST_BODY_EXAMPLE = {
    "refreshToken": "f4Xzh6M4syUf6jZPZizF0FFlC4vuO2HHLHj3GiZHDok"
}

RESPONSE_EXAMPLE = {
    "tokenType": "Bearer",
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
                   "eyJpZCI6IjAxSjVXWDNXVkNGTVhFWVc1NEoxUFlDSFJL"
                   "IiwiZGF0ZV9vbiI6IjIwMjQtMDgtMjQgMTc6Mjk6MzYuNTk"
                   "3MDM5KzAwOjAwIiwiZXhwIjoxNzI0NTIxNDc2fQ.qRUrXC"
                   "xuC99sljk7k4O-ElYsDGk7ck3DHkAfirdZC7E",
    "expiresIn": 900
}


@dataclass
class UpdateAccessTokenOperation(Operation):
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
                            "refreshToken": JWTParameterSchema.refresh_token
                        },
                        required=("refreshToken",)
                    ),
                    example=REQUEST_BODY_EXAMPLE
                ),
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
                                "tokenType": JWTParameterSchema.token_type,
                                "accessToken": JWTParameterSchema.access_token,
                                "expiresIn": JWTParameterSchema.expire_in
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
                        example=FORBIDDEN_EXCEPTION
                    )
                }
            )
        }
