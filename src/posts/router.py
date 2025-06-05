from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_session
from src.posts.schemas import PostListReadSchema, PostQuerySchema
from src.posts.service import PostService

posts_router = APIRouter(prefix="/post", tags=["Посты"])


# MARK: Get
@posts_router.get(path="", summary="Получить список постов")
async def get_posts_route(
    query: PostQuerySchema = Query(),
    session: AsyncSession = Depends(get_session),
) -> PostListReadSchema:
    """
    Получить список постов, а также их общее количество с учётом фильтрации.

    Сортировка постов выполняется с использованием `ts_rank`,
    если задан поисковый запрос `search_query`,
    в противном случае - по дате создания.
    """

    return await PostService.get_posts(query=query, session=session)
