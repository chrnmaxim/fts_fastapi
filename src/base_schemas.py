"""Модуль основных Pydantic схем."""

from pydantic import BaseModel, Field

from src import api_constants


class BaseQuerySchema(BaseModel):
    """Схема query-параметров для пагинации."""

    offset: int | None = Field(
        default=api_constants.DEFAULT_QUERY_OFFSET,
        description="Смещение выборки",
    )
    limit: int | None = Field(
        default=api_constants.DEFAULT_QUERY_LIMIT,
        description="Размер выборки",
    )
    asc: bool = Field(
        default=True,
        description="Порядок сортировки записей по выбранному полю",
    )


class BaseListReadSchema(BaseModel):
    """Основная схема для отображение данных в списке."""

    count: int = Field(
        description="Общее число записей, соответствующих "
        "заданным параметрам фильтрации"
    )
