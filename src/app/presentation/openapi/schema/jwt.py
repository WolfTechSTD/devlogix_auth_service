from dataclasses import dataclass

from litestar.openapi.spec import Schema, OpenAPIType


@dataclass
class JWTParameterSchema:
    token_type: Schema = Schema(
        type=OpenAPIType.STRING,
        description="Тип токена"
    )
    access_token: Schema = Schema(
        type=OpenAPIType.STRING,
        description="Токен доступа"
    )
    expire_in: Schema = Schema(
        type=OpenAPIType.INTEGER,
        description="Время действия токена"
    )
    refresh_token: Schema = Schema(
        type=OpenAPIType.STRING,
        description="Токен обновления"
    )
