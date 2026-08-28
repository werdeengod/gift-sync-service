from typing import TYPE_CHECKING

from src.domain.ports.database import UoWPort

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyUoW(UoWPort):
    def __init__(self, session: 'AsyncSession'):
        self.session = session

    async def begin(self):
        await self.session.begin()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
