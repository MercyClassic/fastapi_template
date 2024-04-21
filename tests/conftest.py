import asyncio
import os
from collections.abc import AsyncGenerator, Generator

import pytest
from dishka import Scope, make_async_container, provide
from dishka.integrations.fastapi import setup_dishka
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.infrastructure.database.database import Base
from app.main.di.providers.core import CoreProvider
from app.main.main import app


class TestProvider(CoreProvider):  # type: ignore[misc]
    @provide(scope=Scope.APP)
    async def get_async_session_maker(
            self,
    ) -> async_sessionmaker[AsyncSession]:
        engine = create_async_engine(
            os.environ['test_db_uri'],
            poolclass=NullPool,
        )
        return async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @provide(scope=Scope.REQUEST)
    async def get_async_session(
            self,
            async_session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncGenerator[AsyncSession, None]:
        async with async_session_maker() as session:
            yield session


@pytest.fixture(scope='session')
async def test_engine() -> AsyncEngine:
    return create_async_engine(
        os.environ['test_db_uri'],
        poolclass=NullPool,
    )


@pytest.fixture(autouse=True, scope='module')
async def _prepare_database(
        test_engine: AsyncEngine,
) -> AsyncGenerator[None, None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope='session')
async def _override_container() -> None:
    container = make_async_container(TestProvider())
    setup_dishka(container=container, app=app)


@pytest.fixture(scope='module')
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test/') as client:
        yield client
