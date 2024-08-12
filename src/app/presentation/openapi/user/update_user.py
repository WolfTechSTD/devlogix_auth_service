from dataclasses import dataclass

from litestar.openapi.spec import (
    OpenAPIMediaType,
    Operation,
    RequestBody,
    Schema,
    OpenAPIResponse,
    OpenAPIType,
    Example,
    Parameter,
)

DESCRIPTION = """
Обновление пользователя.

* **username** - Юзернейм

* **email** - E-mail

* **password** - Пароль

* **isActive** - Статус пользователя
"""

SUMMARY = "Обновление пользователя"


@dataclass
class UpdateUserOperation(Operation):
    def __post_init__(self):
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
                                description="Юзернейм",
                            ),
                            "email": Schema(
                                type=OpenAPIType.STRING,
                                description="E-mail"
                            ),
                            "password": Schema(
                                type=OpenAPIType.STRING,
                                description="Пароль"
                            ),
                            "isActive": Schema(
                                type=OpenAPIType.BOOLEAN,
                                description="Статус пользователя"
                            )
                        }
                    ),
                    example={
                        "username": "User",
                        "email": "user@gmail.com",
                        "password": "UserPassword",
                        "isActive": True
                    }
                )
            }
        )
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
                        examples={
                            "Пользователь не найден": Example(
                                value={
                                    "status_code": 404,
                                    "detail": "Пользователь не найден"
                                }
                            ),
                            "Пользователь с юзернейм уже существует": Example(
                                value={
                                    "status_code": 400,
                                    "detail": "Пользователь с таким "
                                              "юзернейм уже существует"
                                }
                            ),
                            "Пользователь с почтой уже существует": Example(
                                value={
                                    "status_code": 400,
                                    "detail": "Пользователь с такой "
                                              "почтой уже существует"
                                }
                            )
                        }
                    )
                }
            ),
            "403": OpenAPIResponse(
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
                            "status_code": 403,
                            "detail": "Доступ запрещен"
                        }
                    )
                }
            )
        }
