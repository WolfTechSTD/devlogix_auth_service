from dataclasses import dataclass

from litestar.openapi.spec import (
    Operation,
    OpenAPIMediaType,
    Schema,
    OpenAPIType,
    OpenAPIResponse,
)

from app.presentation.openapi.exception import FORBIDDEN_EXCEPTION
from app.presentation.openapi.schema.base import BaseParameters

DESCRIPTION = """
Обновление токена доступа.

* **refreshToken** - Токен обновления
"""

SUMMARY = "Обновление токена доступа"

REQUEST_BODY_EXAMPLE = {
    "refreshToken": "f4Xzh6M4syUf6jZPZizF0FFlC4vuO2HHLHj3GiZHDok"
}


@dataclass
class UpdateAccessTokenInCookie(Operation):
    def __post_init__(self) -> None:
        self.tags = ["auth"]
        self.summary = SUMMARY
        self.description = DESCRIPTION
        self.request_body = None
        self.responses = {
            "204": None,
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
