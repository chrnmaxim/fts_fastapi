"""Основной модуль `conftest` тестов."""

import asyncio
from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from src.database import SessionLocal, engine


# MARK: DBSession
@pytest.fixture(scope="function")
async def session() -> AsyncGenerator[AsyncSession, None]:
    """
    Фикстура AsyncGenerator экземпляра `AsyncSession`.

    Параметр `scope="function"` обеспечивает запуск этой фикстуры перед запуском каждого
    теста.
    После запуска каждого теста, данные в БД откатываются, каждый тест работает
    изолированно от других.
    """

    async with engine.connect() as conn:
        tsx = await conn.begin()
        async with SessionLocal(bind=conn) as session:
            nested_tsx = await conn.begin_nested()

            yield session

            if nested_tsx.is_active:
                await nested_tsx.rollback()
            await tsx.rollback()


# MARK: Loop
@pytest.fixture(scope="session")
def event_loop(request):
    """
    Фикстура для контроля цикла событий.

    Параметр `scope="session"` позволяет pytest иметь только один активный
    цикл событий в течение всей сессии тестов.
    """

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
