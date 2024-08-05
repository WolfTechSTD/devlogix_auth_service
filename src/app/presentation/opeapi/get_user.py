from dataclasses import dataclass

from litestar.openapi.spec import (
    Operation,
    OpenAPIMediaType,
    Parameter,
    Schema,
    OpenAPIType,
    OpenAPIResponse,
)

DESCRIPTION = """
Получение пользователя

* **user_id** - уникальный идентификатор
"""

SUMMARY = "Получение пользователя"


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
            schema=Schema(
                type=OpenAPIType.STRING,
                description="Уникальный идентификатор",
                default="01J4HC5WQB3FK3FA1FMXYVYJ6Y"
            )
        )]
        self.responses = {
            "200": OpenAPIResponse(
                description="Ok",
                content={
                    "json": OpenAPIMediaType(
                        schema=Schema(
                            type=OpenAPIType.OBJECT,
                            properties={
                                "id": Schema(
                                    type=OpenAPIType.STRING,
                                    description="Уникальный идентификатор"
                                ),
                                "username": Schema(
                                    type=OpenAPIType.STRING,
                                    description="Юзернейм"
                                ),
                                "email": Schema(
                                    type=OpenAPIType.STRING,
                                    description="E-mail"
                                )
                            }
                        ),
                        example={
                            "id": "01J4HC5WQB3FK3FA1FMXYVYJ6Y",
                            "username": "User",
                            "email": "user@gmail.com"
                        }
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
                                "status_code": Schema(
                                    type=OpenAPIType.INTEGER,
                                    description="Статус-код HTTP"
                                ),
                                "detail": Schema(
                                    type=OpenAPIType.STRING,
                                    description="Описание ошибки"
                                )
                            }
                        ),
                        example={
                            "status_code": 404,
                            "detail": "Пользователь не найден"
                        }
                    )
                }
            )
        }
