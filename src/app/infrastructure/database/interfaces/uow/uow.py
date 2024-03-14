from sqlalchemy.ext.asyncio import AsyncSession


class UoWInterface:
    session: AsyncSession

    async def commit(self) -> None:
        raise NotImplementedError

    async def rollback(self) -> None:
        raise NotImplementedError
