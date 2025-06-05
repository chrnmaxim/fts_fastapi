"""Модуль Pydantic схем для постов."""

import uuid
from enum import Enum

from pydantic import BaseModel, Field

from src.base_schemas import BaseListReadSchema, BaseQuerySchema


# MARK: Enum
class PostCategoryEnum(str, Enum):
    """Класс для выбора категории поста."""

    countries = "countries"
    cars = "cars"
    movies = "movies"


# MARK: Post
class PostReadSchema(BaseModel):
    """Схема для отображения поста."""

    id: uuid.UUID = Field(description="id поста в БД")
    category: PostCategoryEnum = Field(description="Категория поста")
    content: str = Field(description="Текст поста")
    words_count: int = Field(description="Количество слов в тексте поста")
    unique_tags: list[str] = Field(description="Список уникальных тегов")


class PostListReadSchema(BaseListReadSchema):
    """Схема для отображения списка постов."""

    posts: list[PostReadSchema]


# MARK: Query
class PostQuerySchema(BaseQuerySchema):
    """Схема query-параметров для запроса списка постов."""

    search_query: str | None = Field(default=None, description="Поисковый запрос")
    categories: list[PostCategoryEnum] | None = Field(
        default=None, description="Список категорий постов"
    )
