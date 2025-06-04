from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import SessionLocal


# MARK: Database
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    AsyncGenerator экземпляра `AsyncSession`.

    Выполняет `rollback` текущей транзакции, в случае любого исключения.
    Сессия закрывается внутри контекстного менеджера автоматически.

    Коммит транзакции выполняется автоматически
    при закрытии контекстного менеджера.
    """

    async with SessionLocal.begin() as session:
        try:
            yield session
        except Exception as ex:
            raise ex
