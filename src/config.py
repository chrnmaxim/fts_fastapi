"""Модуль переменных окружения API."""

from os.path import abspath, dirname, join
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE_PATH = join(dirname(abspath(__file__)), ".env")


class ApiSettings(BaseSettings):
    """Класс переменных окружения пакета API."""

    # MARK: API
    DEPLOY_MODE: Literal["DEV", "TEST"]
    APP_VERSION: str = "0.1.0"

    # MARK: Postgres
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POOL_SIZE: int
    MAX_OVERFLOW: int

    @property
    def DATABASE_URL(self):
        """Возвращает URL базы данных."""

        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    POSTS_CONTENT_PRIMARY_LANGUAGE: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        extra="allow",
    )


api_settings = ApiSettings()
