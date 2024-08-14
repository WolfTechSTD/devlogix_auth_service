from dataclasses import dataclass

from litestar.openapi.spec import (
    Operation,
    Schema,
    OpenAPIType,
    Parameter,
    OpenAPIResponse,
    OpenAPIMediaType,
)

from app.presentation.constants import OFFSET, LIMIT, TOTAL
from app.presentation.openapi.schema.base import BaseParameters
from app.presentation.openapi.exceptions.base import FORBIDDEN_EXCEPTION
from app.presentation.openapi.security.base import BEARER_TOKEN
from app.presentation.openapi.schema.user import UserParameterSchema

DESCRIPTION = """
Получение пользователей.

* **limit** - Лимит записей

* **offset** - Текущая запись
"""

SUMMARY = "Получение пользователей"

RESPONSE_EXAMPLE = {
    "limit": LIMIT,
    "offset": OFFSET,
    "total": TOTAL,
    "values": [
        {
            "id": "01J4HC5WQB3FK3FA1FMXYVYJ6Y",
            "username": "User1",
            "email": "user1@gmail.com",
            "isActive": True
        },
        {
            "id": "05J4HC5WQB3FK3FA1FMXYGFJ7B",
            "username": "User2",
            "email": "user2@gmail.com",
            "isActive": True
        }
    ]
}


@dataclass
class GetUsersOperation(Operation):
    def __post_init__(self) -> None:
        self.tags = ["users"]
        self.summary = SUMMARY
        self.security = [BEARER_TOKEN]
        self.description = DESCRIPTION
        self.parameters = [
            Parameter(
                name="limit",
                param_in="query",
                required=False,
                schema=Schema(
                    type=OpenAPIType.INTEGER,
                    description="Лимит записей",
                    default=LIMIT
                )
            ),
            Parameter(
                name="offset",
                param_in="query",
                required=False,
                schema=Schema(
                    type=OpenAPIType.INTEGER,
                    description="Текущая страница",
                    default=OFFSET
                )
            )
        ]
        self.responses = {
            "200": OpenAPIResponse(
                description="Ok",
                content={
                    "json": OpenAPIMediaType(
                        schema=Schema(
                            type=OpenAPIType.OBJECT,
                            properties={
                                "limit": BaseParameters.limit,
                                "offset": BaseParameters.offset,
                                "total": BaseParameters.total,
                                "values": Schema(
                                    type=OpenAPIType.OBJECT,
                                    description="Пользователи",
                                    properties={
                                        "id": UserParameterSchema.id,
                                        "username": UserParameterSchema.username,
                                        "email": UserParameterSchema.email,
                                        "isActive": UserParameterSchema.is_active
                                    }
                                )
                            }
                        ),
                        example=RESPONSE_EXAMPLE
                    ),
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
