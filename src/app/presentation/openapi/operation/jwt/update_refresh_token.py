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
Обновление токена обновления.

* **refreshToken** - Токен обновления
"""

SUMMARY = "Обновление токена обновления"

REQUEST_BODY_EXAMPLE = {
    "refreshToken": "f4Xzh6M4syUf6jZPZizF0FFlC4vuO2HHLHj3GiZHDok"
}

RESPONSE_EXAMPLE = {
    "refreshToken": "f4Xzh6M4syUf6jZPZizF0FFlC4vuO2HHLHj3GiZHDok"
}


@dataclass
class UpdateRefreshTokenOperation(Operation):
    def __post_init__(self) -> None:
        self.tags = ["jwt"]
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
                                "refreshToken": JWTParameterSchema.refresh_token
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
