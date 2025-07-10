# tests/conftest.py

import os
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from blog.infra.database import Base
from blog.api.main import app
from blog.api import deps
from asgi_lifespan import LifespanManager

TEST_DATABASE_URL = os.getenv(
    "DATABASE_URL_TEST",
    "postgresql+asyncpg://test_user:test_password@db_test:5432/blog_test",
)


@pytest_asyncio.fixture(scope="session")
def event_loop():
    import asyncio

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def setup_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    async_session = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine, async_session


@pytest_asyncio.fixture
async def db_session(setup_engine):
    _, async_session = setup_engine
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_db_session():
        yield db_session

    app.dependency_overrides[deps.get_db_session] = override_get_db_session

    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        # Adiciona follow_redirects=True aqui
        async with AsyncClient(transport=transport, base_url="http://test", follow_redirects=True) as ac: 
            yield ac

    app.dependency_overrides.clear()