"""Модуль конфигурации API."""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from src.config import api_settings
from src.posts.router import posts_router

app = FastAPI(
    title="FTS Project Template",
    version=api_settings.APP_VERSION,
    description="Реализация полнотекстового поиска FastAPI + SQLAlchemy + PostgreSQL",
)

available_routers = [posts_router]
for router in available_routers:
    app.include_router(
        router=router,
        prefix="/api/v1",
    )


@app.get(
    path="/",
    response_class=HTMLResponse,
    include_in_schema=False,
)
def home():
    return f"""
    <html>
    <head><title>FTS Project Template</title></head>
    <body>
    <h1>FTS Project Template в режиме {api_settings.DEPLOY_MODE}</h1>
    <ul>
    <li><a href="/docs">Документация Swagger</a></li>
    <li><a href="/redoc">Документация ReDoc</a></li>
    </ul>
    </body>
    </html>
    """
