import asyncio
import os
from functools import partial
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.infrastructure.database.database import Base
from app.main.di.dependencies.stub import get_session_stub
from app.main.main import app


def create_test_async_session_maker(engine: AsyncEngine):
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )


test_engine = create_async_engine(
    os.environ['test_db_uri'],
    poolclass=NullPool,
)
test_async_session_maker = create_test_async_session_maker(
    test_engine,
)


async def override_get_async_session(
    test_async_session_maker: async_sessionmaker,
) -> AsyncGenerator:
    async with test_async_session_maker() as session:
        yield session


app.dependency_overrides[get_session_stub] = partial(
    override_get_async_session,
    test_async_session_maker,
)


@pytest.fixture(scope='module')
async def test_session() -> AsyncSession:
    async with test_async_session_maker() as session:
        yield session


@pytest.fixture(autouse=True, scope='module')
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='module')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='module')
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test/') as client:
        yield client
