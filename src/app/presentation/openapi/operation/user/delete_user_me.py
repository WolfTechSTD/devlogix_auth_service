from dataclasses import dataclass

from litestar.openapi.spec import (
    OpenAPIMediaType,
    Operation,
    Schema,
    OpenAPIResponse,
    OpenAPIType,
)

from app.presentation.openapi.exceptions.base import FORBIDDEN_EXCEPTION
from app.presentation.openapi.schema.base import BaseParameters
from app.presentation.openapi.security.base import BEARER_TOKEN

DESCRIPTION = "Удаление аккаунта."

SUMMARY = "Удаление аккаунта."


@dataclass
class DeleteUserMeOperation(Operation):
    def __post_init__(self) -> None:
        self.tags = ["users"]
        self.summary = SUMMARY
        self.description = DESCRIPTION
        self.security = [BEARER_TOKEN]
        self.responses = {
            "204": OpenAPIResponse(
                description="Not Content",
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
                        example=FORBIDDEN_EXCEPTION
                    )
                }
            )
        }
