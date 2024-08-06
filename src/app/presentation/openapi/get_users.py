from dataclasses import dataclass

from litestar.openapi.spec import (
    Operation,
    Schema,
    OpenAPIType,
    Parameter,
    OpenAPIResponse,
    OpenAPIMediaType,
)

DESCRIPTION = """
Получение пользователей

* **limit** - лимит записей

* **offset** - текущая запись
"""

SUMMARY = "Получение пользователей"

LIMIT = 10

OFFSET = 0

TOTAL = 2


@dataclass
class GetUsersOperation(Operation):
    def __post_init__(self) -> None:
        self.tags = ["users"]
        self.summary = SUMMARY
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
                                "limit": Schema(
                                    type=OpenAPIType.INTEGER,
                                    description="Лимит записей"
                                ),
                                "offset": Schema(
                                    type=OpenAPIType.INTEGER,
                                    description="Текущая страница"
                                ),
                                "total": Schema(
                                    type=OpenAPIType.INTEGER,
                                    description="Количество записей"
                                ),
                                "values": Schema(
                                    type=OpenAPIType.OBJECT,
                                    description="Пользователи",
                                    properties={
                                        "id": Schema(
                                            type=OpenAPIType.STRING,
                                            description="Уникальный "
                                                        "идентификатор"
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
                                )
                            }
                        ),
                        example={
                            "limit": LIMIT,
                            "offset": OFFSET,
                            "total": TOTAL,
                            "values": [
                                {
                                    "id": "01J4HC5WQB3FK3FA1FMXYVYJ6Y",
                                    "username": "User1",
                                    "email": "user1@gmail.com"
                                },
                                {
                                    "id": "05J4HC5WQB3FK3FA1FMXYGFJ7B",
                                    "username": "User2",
                                    "email": "user2@gmail.com"
                                }
                            ]
                        }
                    ),
                }
            )
        }
