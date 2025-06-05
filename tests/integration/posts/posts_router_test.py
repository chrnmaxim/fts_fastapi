"""Модуль для тестирования эндпоинтов роутера src.posts.router.posts_router."""

import re
from datetime import datetime, timedelta, timezone

import httpx
from fastapi import status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.posts.models import PostModel
from src.posts.router import posts_router
from src.posts.schemas import PostCategoryEnum, PostListReadSchema
from tests import test_constants
from tests.integration.conftest import BaseTestRouter


class TestPostsRouter(BaseTestRouter):
    """Класс для тестирования эндпоинтов роутера src.posts.router.posts_router."""

    router = posts_router

    # MARK: Get
    async def test_get_posts_no_query(self, router_client: httpx.AsyncClient):
        """Возможно получить список постов без использования фильтрации."""

        response = await router_client.get(url="/posts")
        assert response.status_code == status.HTTP_200_OK

        posts_data = PostListReadSchema(**response.json())
        assert posts_data.count == test_constants.POSTS_COUNT

        post_data = posts_data.posts[0]
        assert post_data.id is not None
        assert post_data.category is not None
        assert post_data.content is not None

        tag_pattern = re.compile(r"#(\w+)")
        words: list[str] = re.findall(r"\w+", post_data.content.lower())
        tags: list[str] = tag_pattern.findall(post_data.content)

        assert post_data.words_count == len(words)
        assert post_data.unique_tags == list(set(tags))

    async def test_get_posts_empty_query(
        self,
        router_client: httpx.AsyncClient,
        session: AsyncSession,
    ):
        """
        Возможно получить пустой список постов,
        если нет записей, удовлетворяющих параметрам поиска.
        """

        # Удаляем все посты категории cars
        stmt = delete(PostModel).where(PostModel.category == PostCategoryEnum.cars)
        await session.execute(stmt)
        await session.commit()

        response = await router_client.get(
            url="/posts", params={"categories": [PostCategoryEnum.cars.value]}
        )
        assert response.status_code == status.HTTP_200_OK

        posts_data = PostListReadSchema(**response.json())
        assert posts_data.count == 0
        assert posts_data.posts == []

    async def test_get_posts_category_query(
        self,
        router_client: httpx.AsyncClient,
        session: AsyncSession,
    ):
        """
        Возможно получить список постов
        c использованием фильтрации по категории.
        """

        # Для любого поста устанавливаем дату создания
        # как день назад для проверки сортировки по дате создания.
        day_ago = datetime.now(timezone.utc) - timedelta(days=1)
        stmt = select(PostModel).limit(1)
        result = await session.execute(stmt)
        post_db = result.scalar_one()
        post_db.created_at = day_ago
        await session.commit()

        response = await router_client.get(
            url="/posts", params={"categories": [post_db.category]}
        )
        assert response.status_code == status.HTTP_200_OK

        posts_data = PostListReadSchema(**response.json())
        assert posts_data.count == test_constants.POSTS_PER_CATEGORY_COUNT

        post_data = posts_data.posts[0]
        assert post_data.id == post_db.id
        assert post_data.category == post_db.category
        assert post_data.content == post_db.content

    async def test_get_posts_search_query(self, router_client: httpx.AsyncClient):
        """
        Возможно получить список постов
        c использованием полнотекстового поиска.
        """

        response = await router_client.get(
            url="/posts",
            params={
                "search_query": [test_constants.POST_CONTENT_KEYWORD],
            },
        )
        assert response.status_code == status.HTTP_200_OK

        posts_data = PostListReadSchema(**response.json())
        assert posts_data.count == 1

        post_data = posts_data.posts[0]
        assert post_data.id is not None
        assert post_data.category == PostCategoryEnum.cars
        assert test_constants.POST_CONTENT_KEYWORD in post_data.content
