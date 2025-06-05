"""Модуль моделей постов."""

import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TEXT, TSVECTOR, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.api_constants import CURRENT_TIMESTAMP_UTC
from src.database import Base


class PostModel(Base):
    """Модель поста."""

    __tablename__ = "posts"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    category: Mapped[str] = mapped_column(
        sa.String,
        index=True,
        comment="Категория поста",
    )
    content: Mapped[str] = mapped_column(TEXT, comment="Текст поста")
    search_vector: Mapped[str] = mapped_column(
        TSVECTOR, comment="Вектор для полнотекстового поиска"
    )
    created_at: Mapped[datetime] = mapped_column(
        sa.TIMESTAMP(timezone=True),
        index=True,
        server_default=CURRENT_TIMESTAMP_UTC,
    )

    __table_args__ = (
        sa.Index(
            "posts_search_vector_idx",
            "search_vector",
            postgresql_using="gin",
        ),
    )
