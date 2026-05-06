.PHONY: install run test test-unit test-integration test-isolated test-integration-isolated test-integration-isolated-down lint format typecheck migrate migration revision docker-build up down logs shell

PYTHONPATH ?= src
export PYTHONPATH

install:
	poetry install --with dev

run:
	poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	poetry run pytest

test-unit:
	poetry run pytest tests/unit -v

test-integration:
	poetry run pytest tests/integration -v

test-integration-isolated test-isolated:
	docker compose -f docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from test_runner test_runner

test-integration-isolated-down:
	docker compose -f docker-compose.test.yml down -v

lint:
	poetry run flake8 src tests

format:
	poetry run black src tests

typecheck:
	poetry run mypy src

migrate:
	poetry run alembic upgrade head

revision:
	poetry run alembic revision --autogenerate -m "$(name)"

migration: revision

docker-build:
	docker build -t fastapi-clean-architecture:latest .

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f api

shell:
	docker compose exec api /bin/sh
