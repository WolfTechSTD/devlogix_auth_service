from dataclasses import dataclass

from litestar.openapi.spec import (
    OpenAPIMediaType,
    Operation,
    RequestBody,
    Schema,
    OpenAPIResponse,
    OpenAPIType,
)

DESCRIPTION = """
Создание пользователя.

* **username** - юзернейм

* **email** - e-mail

* **password** - пароль
"""

SUMMARY = "Создание пользователя"


@dataclass
class CreateUserOperation(Operation):
    def __post_init__(self) -> None:
        self.tags = ["users"]
        self.summary = SUMMARY
        self.description = DESCRIPTION
        self.request_body = RequestBody(
            content={
                "json": OpenAPIMediaType(
                    schema=Schema(
                        type=OpenAPIType.OBJECT,
                        properties={
                            "username": Schema(
                                type=OpenAPIType.STRING,
                                description="Юзернейм"
                            ),
                            "email": Schema(
                                type=OpenAPIType.STRING,
                                description="E-mail"
                            ),
                            "password": Schema(
                                type=OpenAPIType.STRING,
                                description="Пароль"
                            )
                        }
                    ),
                    example={
                        "username": "User",
                        "email": "user@gmail.com",
                        "password": "UserPassword"
                    },
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
                                ),
                                "isActive": Schema(
                                    type=OpenAPIType.BOOLEAN,
                                    description="Статус пользователя"
                                )
                            }
                        ),
                        example={
                            "id": "01J4HC5WQB3FK3FA1FMXYVYJ6Y",
                            "username": "User",
                            "email": "user@gmail.com",
                            "isActive": True
                        }
                    )
                }
            ),
            "400": OpenAPIResponse(
                description="Bad Request",
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
                            "status_code": 400,
                            "detail": "Пользователь уже существует"
                        }
                    )
                }
            )
        }
