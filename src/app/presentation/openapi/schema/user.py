from dataclasses import dataclass

from litestar.openapi.spec import (
    Schema,
    OpenAPIType,
)


@dataclass
class UserParameterSchema:
    id: Schema = Schema(
        type=OpenAPIType.STRING,
        description="Уникальный идентификатор"
    )
    username: Schema = Schema(
        type=OpenAPIType.STRING,
        description="Юзернейм"
    )
    email: Schema = Schema(
        type=OpenAPIType.STRING,
        description="E-mail"
    )
    user_id: Schema = Schema(
        type=OpenAPIType.STRING,
        description="Уникальный идентификатор",
        default="01J4HC5WQB3FK3FA1FMXYVYJ6Y"
    )
    is_active: Schema = Schema(
        type=OpenAPIType.BOOLEAN,
        description="Статус пользователя"
    )
    password: Schema = Schema(
        type=OpenAPIType.STRING,
        description="Пароль"
    )
