from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession


class UoWInterface(Protocol):
    session: AsyncSession

    async def commit(self) -> None:
        raise NotImplementedError

    async def rollback(self) -> None:
        raise NotImplementedError


class UoW(UoWInterface):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
