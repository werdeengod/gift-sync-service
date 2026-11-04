from typing import Optional
from collections.abc import AsyncIterable
from dishka import Provider, Scope, provide, FromDishka
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.domain.ports.database import UoWPort
from src.infrastructure.database import SQLAlchemyUoW, Base
from src.infrastructure.serializers import json_serializer


class DatabaseProvider(Provider):
    def __init__(self, db_url: Optional[str] = None):
        super().__init__()
        self.db_url = db_url

    @provide(scope=Scope.APP)
    async def get_engine(self) -> AsyncIterable[async_sessionmaker[AsyncSession]]:
        engine = create_async_engine(
            self.db_url,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            echo=True,
            json_serializer=json_serializer
        )

        session_maker = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        try:
            yield session_maker
        finally:
            await engine.dispose()

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self,
        session_maker: FromDishka[async_sessionmaker[AsyncSession]]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            try:
                yield session
            finally:
                await session.close()

    @provide(scope=Scope.REQUEST, provides=UoWPort)
    async def get_uow(self, session: FromDishka[AsyncSession]) -> SQLAlchemyUoW:
        return SQLAlchemyUoW(session)
