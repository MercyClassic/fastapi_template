from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def create_async_session_maker(
        database_url: str,
) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(
        database_url,
        isolation_level='REPEATABLE READ',
    )
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def get_async_session(
        async_session_maker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
