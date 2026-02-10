import os
from collections.abc import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.infrastructure.database.transaction import (
    TransactionManager,
    TransactionManagerInterface,
)


class DbProvider(Provider):  # type: ignore[misc]
    scope = Scope.REQUEST
    component = 'db'

    @provide(scope=Scope.APP)
    async def get_async_session_maker(
        self,
    ) -> async_sessionmaker[AsyncSession]:
        engine = create_async_engine(
            os.environ['DB_URI'],
            isolation_level='REPEATABLE READ',
        )
        return async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @provide
    async def get_async_session(
        self,
        async_session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncGenerator[AsyncSession, None]:
        async with async_session_maker() as session:
            yield session

    @provide
    async def get_transaction_manager(
        self,
        session: AsyncSession,
    ) -> TransactionManagerInterface:
        return TransactionManager(session)
