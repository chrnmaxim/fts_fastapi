"""Модуль констант API."""

from sqlalchemy import TextClause, text

# MARK: Database
CURRENT_TIMESTAMP_UTC: TextClause = text("(CURRENT_TIMESTAMP AT TIME ZONE 'UTC')")
DEFAULT_QUERY_OFFSET: int = 0
DEFAULT_QUERY_LIMIT: int = 100
