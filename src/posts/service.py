"""Модуль сервисных методов для работы с постами."""

import re

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import api_settings
from src.posts.models import PostModel
from src.posts.schemas import PostListReadSchema, PostQuerySchema, PostReadSchema


class PostService:
    """
    Класс для работы с постами.

    Позволяет выполнять CRUD операции.
    """

    # MARK: Utils
    @classmethod
    def _process_post_data(cls, post_content: str) -> tuple[int, list[str]]:
        """
        Обработать данные текста поста: получить количество слов
        в тексте и список уникальных тегов.
        """

        tag_pattern = re.compile(r"#(\w+)")
        words: list[str] = re.findall(r"\w+", post_content.lower())
        tags: list[str] = tag_pattern.findall(post_content)

        return len(words), list(set(tags))

    # MARK: Read
    @classmethod
    async def get_posts(
        cls,
        query: PostQuerySchema,
        session: AsyncSession,
    ) -> PostListReadSchema:
        """
        Получить список постов, а также их общее количество с учётом фильтрации.

        Сортировка постов выполняется с использованием `ts_rank`,
        если задан поисковый запрос `search_query`,
        в противном случае - по дате создания.
        """

        stmt = select(PostModel.id, PostModel.category, PostModel.content)

        if query.categories:
            stmt = stmt.where(PostModel.category.in_(query.categories))

        if query.search_query:
            keywords = query.search_query.split()
            ts_query = func.to_tsquery(
                api_settings.POSTS_CONTENT_PRIMARY_LANGUAGE,
                " | ".join(keywords),
            )
            stmt = stmt.where(PostModel.search_vector.op("@@")(ts_query))

        count_stmt = select(func.count()).select_from(stmt.subquery())
        count = await session.scalar(count_stmt) or 0

        posts: list[PostReadSchema] = []
        if count > 0:
            if query.search_query:
                stmt = stmt.add_columns(
                    func.ts_rank(PostModel.search_vector, ts_query).label("rank")
                )
                order_by_field = stmt.selected_columns.rank
            else:
                order_by_field = PostModel.created_at

            stmt = stmt.order_by(order_by_field).offset(query.offset).limit(query.limit)
            posts_data_result = await session.stream(stmt)

            async for post_data_result in posts_data_result:
                post_data = post_data_result._mapping
                words_count, unique_tags = cls._process_post_data(
                    post_content=post_data["content"]
                )
                posts.append(
                    PostReadSchema(
                        **post_data, words_count=words_count, unique_tags=unique_tags
                    )
                )

        return PostListReadSchema(count=count, posts=posts)
