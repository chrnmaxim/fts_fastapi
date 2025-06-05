ruff_fix:
	uv run ruff format . && uv run ruff check --fix . && uv run ruff check --fix --select I .
ruff_check:
	uv run ruff check . && uv run ruff check --select I . && uv run ruff format --check .
start_dev:
	docker compose --profile dev up -d
stop_dev:
	docker compose --profile dev down
remove_dev:
	docker compose --profile dev down -v
start_local_db:
	docker compose -f docker-compose.yml up -d postgres_fts
stop_local_db:
	docker compose -f docker-compose.yml down postgres_fts
remove_local_db:
	docker compose -f docker-compose.yml down -v postgres_fts
test:
	docker compose -f docker-compose.yml run --rm fts_fastapi_test
	docker compose -f docker-compose.yml --profile test down --volumes
migrate:
	uv run alembic upgrade heads