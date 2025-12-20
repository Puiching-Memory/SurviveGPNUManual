"""Pytest fixtures for FastAPI backend tests."""

from __future__ import annotations

import os
import sys
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool
from sqlalchemy_utils import create_database, database_exists, drop_database

# ----------------------------------------------------------------------------
# Ensure test settings are loaded and project root is importable
# ----------------------------------------------------------------------------
os.environ.setdefault("ENVIRONMENT", "testing")
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from app.config import Settings, get_settings  # noqa: E402  pylint: disable=wrong-import-position
from app.db import Base  # noqa: E402  pylint: disable=wrong-import-position
from app.db.database import get_db  # noqa: E402  pylint: disable=wrong-import-position
from app.main import app  # noqa: E402  pylint: disable=wrong-import-position

# ---------------------------------------------------------------------------
# Session-scoped helpers
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def settings_instance() -> Settings:
    """Return fresh Settings for the test session."""
    get_settings.cache_clear()
    return get_settings()


@pytest.fixture(scope="session")
def effective_test_db_url(settings_instance: Settings) -> str:
    """Return DB URL for tests (env > default)."""
    url = (settings_instance.TEST_DATABASE_URL or "").strip()
    return url if url and url.lower() != "none" else settings_instance.DATABASE_URL


# ---------------------------------------------------------------------------
# Automatic DB lifecycle for the whole test session
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture(scope="session", autouse=True)
async def _session_db_lifecycle(effective_test_db_url: str):
    is_sqlite = effective_test_db_url.startswith("sqlite")

    created_db = False
    sync_url = None
    if not is_sqlite:
        sync_url = effective_test_db_url.replace("postgresql+asyncpg", "postgresql")
        if not database_exists(sync_url):
            create_database(sync_url)
            created_db = True

    engine = create_async_engine(effective_test_db_url, poolclass=NullPool)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield  # tests run here

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

    if created_db and sync_url:
        drop_database(sync_url)


# ---------------------------------------------------------------------------
# Per-test fixtures
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture()
async def db_session(effective_test_db_url: str) -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(effective_test_db_url, poolclass=NullPool)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        yield session
    await engine.dispose()


@pytest_asyncio.fixture()
async def test_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    def _override_get_db() -> Generator[AsyncSession, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    app.dependency_overrides.pop(get_db, None)
