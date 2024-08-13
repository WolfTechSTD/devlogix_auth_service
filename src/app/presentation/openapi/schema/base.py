from dataclasses import dataclass

from litestar.openapi.spec import (
    Schema,
    OpenAPIType,
)


@dataclass
class BaseParameters:
    status_code: Schema = Schema(
        type=OpenAPIType.INTEGER,
        description="Статус-код HTTP"
    )
    detail: Schema = Schema(
        type=OpenAPIType.STRING,
        description="Описание ошибки"
    )
    limit: Schema = Schema(
        type=OpenAPIType.INTEGER,
        description="Лимит записей"
    )
    offset: Schema = Schema(
        type=OpenAPIType.INTEGER,
        description="Текущая страница"
    )
    total: Schema = Schema(
        type=OpenAPIType.INTEGER,
        description="Количество записей"
    )
