"""Модуль `conftest` с фикстурами для пакета `tasks.integration`."""

from typing import AsyncGenerator

import httpx
import pytest_asyncio
from fastapi import APIRouter, FastAPI

from src.dependencies import get_session


class BaseTestRouter:
    """Класс для тестирования эндпоинтов."""

    router: APIRouter

    @pytest_asyncio.fixture(scope="function")
    async def router_client(self, session) -> AsyncGenerator[httpx.AsyncClient, None]:
        """
        `AsyncGenerator` для экземпляра `httpx.AsyncClient`.

        Конфигурирует `httpx.ASGITransport` для перенаправления всех запросов
        напрямую в API с использованием протокола ASGI.
        """

        app = FastAPI()
        app.include_router(self.router)
        app.dependency_overrides[get_session] = lambda: session

        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport, base_url="http://test"
        ) as async_client:
            yield async_client
