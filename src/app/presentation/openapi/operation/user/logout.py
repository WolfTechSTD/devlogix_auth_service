from dataclasses import dataclass

from litestar.openapi.spec import (
    Operation,
    OpenAPIMediaType,
    Schema,
    OpenAPIType,
    OpenAPIResponse,
)

from app.presentation.openapi.exceptions.base import FORBIDDEN_EXCEPTION
from app.presentation.openapi.schema.base import BaseParameters
from app.presentation.openapi.security.base import SESSION

DESCRIPTION = """Разлогирование."""

SUMMARY = "Разлогирование"


@dataclass
class LogoutUserOperation(Operation):
    def __post_init__(self) -> None:
        self.tags = ["users"]
        self.summary = SUMMARY
        self.description = DESCRIPTION
        self.security = [SESSION]
        self.request_body = None
        self.responses = {
            "204": OpenAPIResponse(
                description="No Content",
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
