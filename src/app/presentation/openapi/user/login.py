from dataclasses import dataclass

from litestar.openapi.spec import (
    OpenAPIMediaType,
    Operation,
    RequestBody,
    Schema,
    OpenAPIResponse,
    OpenAPIType,
    Example,
)

DESCRIPTION = """
Аутентификация

* **username** - юзернейм

* **email** - e-mail

* **password** - пароль
"""

SUMMARY = "Аутентификация"


@dataclass
class UserLoginOperation(Operation):
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
                        },
                        required=("password",)
                    ),
                    examples={
                        "Ввода с юзернеймом": Example(
                            value={
                                "username": "User",
                                "password": "UserPassword"
                            }
                        ),
                        "Ввод с e-mail": Example(
                            value={
                                "email": "user@gmail.com",
                                "password": "UserPassword"
                            }
                        )
                    }
                )
            }
        )
        self.responses = {
            "200": OpenAPIResponse(
                description="Ok",
                content=None
            ),
            "403": OpenAPIResponse(
                description="Forbidden",
                content={
                    "json": OpenAPIMediaType(
                        schema=Schema(
                            type=OpenAPIType.OBJECT,
                            properties={
                                "status_code": Schema(
                                    type=OpenAPIType.INTEGER,
                                    description="Статус-код HTTp"
                                ),
                                "detail": Schema(
                                    type=OpenAPIType.STRING,
                                    description="Описание ошибки"
                                )
                            }
                        ),
                        example={
                            "status_code": 403,
                            "detail": "Данные введены неверно"
                        }
                    )
                }
            )
        }
