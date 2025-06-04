from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from src.config import api_settings

app = FastAPI(
    title="FTS Project Template",
    version=api_settings.APP_VERSION,
    description="Реализация полнотекстового поиска FastAPI + SQLAlchemy + PostgreSQL",
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
