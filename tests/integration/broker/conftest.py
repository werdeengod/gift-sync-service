import pytest
import pytest_asyncio

import aio_pika
from dishka import make_async_container, AsyncContainer
from testcontainers.community.rabbitmq import RabbitMqContainer

from src.domain.ports.services import MessageBrokerPort

from src.bootstrap.providers import (
    SerializerProvider,
    EventProvider,
)


@pytest.fixture(scope="session")
def rabbitmq_url():
    with RabbitMqContainer("rabbitmq:4.0-management") as rabbitmq:
        host = rabbitmq.get_container_host_ip()
        port = rabbitmq.get_exposed_port(5672)

        url = f"amqp://guest:guest@{host}:{port}/"

        yield url


@pytest_asyncio.fixture
async def build_container(rabbitmq_url):
    container = make_async_container(
        SerializerProvider(),
        EventProvider(rabbitmq_url)
    )

    yield container

    await container.close()


@pytest_asyncio.fixture
async def message_broker(build_container: 'AsyncContainer'):
    async with build_container() as request:
        broker = await request.get(MessageBrokerPort)
        yield broker
