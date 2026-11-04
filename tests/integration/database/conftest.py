import pytest
import pytest_asyncio

from dishka import make_async_container, AsyncContainer
from testcontainers.community.postgres import PostgresContainer

from src.domain.ports.database import UoWPort
from src.domain.ports.database.repositories import GiftRepositoryPort, OutboxRepositoryPort

from src.bootstrap.providers import (
    DatabaseProvider,
    RepositoryProvider,
    SerializerProvider,
    MapperProvider,
)


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16-alpine", driver="asyncpg") as postgres:
        yield postgres


@pytest_asyncio.fixture
async def build_container(postgres_container):
    db_url = postgres_container.get_connection_url()

    container = make_async_container(
        DatabaseProvider(db_url),
        RepositoryProvider(),
        SerializerProvider(),
        MapperProvider(),
    )

    yield container

    await container.close()


@pytest_asyncio.fixture
async def uow(build_container: AsyncContainer):
    async with build_container() as request:
        uow = await request.get(UoWPort)
        yield uow


@pytest_asyncio.fixture
async def outbox_repository(build_container: AsyncContainer):
    async with build_container() as request:
        repo = await request.get(OutboxRepositoryPort)
        yield repo


@pytest_asyncio.fixture
async def gift_repository(build_container: AsyncContainer):
    async with build_container() as request:
        repo = await request.get(GiftRepositoryPort)
        yield repo

