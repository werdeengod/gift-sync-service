from abc import ABC, abstractmethod
from typing import AsyncContextManager
from contextlib import asynccontextmanager


class UoWPort(ABC):
    @asynccontextmanager
    async def transaction(self) -> AsyncContextManager['UoWPort']:
        await self.begin()

        try:
            yield self
            await self.commit()

        except Exception:
            await self.rollback()
            raise

    @abstractmethod
    async def begin(self):
        pass

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass
