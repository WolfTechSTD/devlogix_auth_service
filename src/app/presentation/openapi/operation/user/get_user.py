from dataclasses import dataclass

from litestar.openapi.spec import (
    Operation,
    OpenAPIMediaType,
    Parameter,
    Schema,
    OpenAPIType,
    OpenAPIResponse,
)

from app.presentation.openapi.schema.base import BaseParameters
from app.presentation.openapi.exceptions.base import FORBIDDEN_EXCEPTION
from app.presentation.openapi.exceptions.user import USER_NOT_FOUND_EXCEPTION
from app.presentation.openapi.security.base import BEARER_TOKEN
from app.presentation.openapi.schema.user import UserParameterSchema

DESCRIPTION = """
Получение пользователя.

* **user_id** - уникальный идентификатор
"""

SUMMARY = "Получение пользователя"

RESPONSE_EXAMPLE = {
    "id": "01J4HC5WQB3FK3FA1FMXYVYJ6Y",
    "username": "User",
    "email": "operation@gmail.com",
    "isActive": True
}


@dataclass
class GetUserOperation(Operation):
    def __post_init__(self) -> None:
        self.tags = ["users"]
        self.summary = SUMMARY
        self.description = DESCRIPTION
        self.parameters = [Parameter(
            name="user_id",
            param_in="path",
            required=True,
            schema=UserParameterSchema.user_id
        )]
        self.security = [BEARER_TOKEN]
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
            "404": OpenAPIResponse(
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
                        example=USER_NOT_FOUND_EXCEPTION
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
