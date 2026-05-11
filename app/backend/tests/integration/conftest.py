"""Integration tests: HTTP client + PostgreSQL + Redis (see README)."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import get_settings
from app.infrastructure.db.base import Base
from app.infrastructure.db.models import order as _order_model  # noqa: F401
from app.infrastructure.db.models import user as _user_model  # noqa: F401


def _ensure_test_env() -> None:
    """Align env with docker-compose defaults for local integration runs."""
    os.environ.setdefault("DB_HOST", "127.0.0.1")
    os.environ.setdefault("DB_PORT", "5432")
    os.environ.setdefault("DB_USER", "app")
    os.environ.setdefault("DB_PASSWORD", "app")
    os.environ.setdefault("DB_NAME", "app")
    os.environ.setdefault("REDIS_HOST", "127.0.0.1")
    os.environ.setdefault("REDIS_PORT", "6379")
    os.environ.setdefault("REDIS_DB", "15")
    os.environ.setdefault(
        "JWT_SECRET_KEY",
        "test-secret-key-at-least-32-chars-long-for-integration",
    )


@pytest_asyncio.fixture
async def engine() -> AsyncIterator[AsyncEngine]:
    """Ensure schema exists; one async engine per test (same loop as HTTP client)."""
    _ensure_test_env()
    get_settings.cache_clear()
    settings = get_settings()
    eng = create_async_engine(settings.db.dsn, pool_pre_ping=True)
    try:
        async with eng.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as exc:  # noqa: BLE001 — surface connection errors
        await eng.dispose()
        pytest.skip(f"PostgreSQL not reachable for integration tests: {exc}")

    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield eng
    finally:
        await eng.dispose()
        get_settings.cache_clear()


@pytest_asyncio.fixture
async def http_client(engine: AsyncEngine) -> AsyncIterator[AsyncClient]:
    """ASGI app + HTTP client share the test's asyncio loop."""
    _ = engine
    get_settings.cache_clear()
    _ensure_test_env()
    from app.main import app

    async with (
        LifespanManager(app),
        AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client,
    ):
        yield client


@pytest_asyncio.fixture(autouse=True)
async def cleanup_between_integration_tests(engine: AsyncEngine) -> AsyncIterator[None]:
    """Avoid cross-test leakage in DB and Redis cache."""
    yield
    async with engine.begin() as conn:
        await conn.execute(text('TRUNCATE TABLE "users" CASCADE'))
    get_settings.cache_clear()
    _ensure_test_env()
    settings = get_settings()
    redis_client = Redis.from_url(settings.redis.url, decode_responses=False)
    await redis_client.flushdb()
    await redis_client.aclose()
