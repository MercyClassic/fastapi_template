from sqlalchemy.ext.asyncio import AsyncSession


class UoWInterface:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self) -> None:
        raise NotImplementedError

    async def rollback(self) -> None:
        raise NotImplementedError
