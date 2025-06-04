from sqlalchemy import AsyncAdaptedQueuePool, MetaData
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.config import api_settings

DB_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


class Base(DeclarativeBase):
    """Основной класс для всех моделей базы данных."""

    metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)


engine = create_async_engine(
    api_settings.DATABASE_URL,
    pool_size=api_settings.POOL_SIZE,
    max_overflow=api_settings.MAX_OVERFLOW,
    poolclass=AsyncAdaptedQueuePool,
    pool_pre_ping=True,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)
