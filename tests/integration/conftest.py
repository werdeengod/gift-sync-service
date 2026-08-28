import pytest
from unittest.mock import AsyncMock

from dishka import make_async_container, Provider, Scope, provide


class MockProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_mock_service(self) -> AsyncMock:
        mock = AsyncMock()
        mock.get_data.return_value = {"data": "test"}
        return mock


@pytest.fixture
def container():
    return make_async_container(MockProvider())


@pytest.fixture
def worker(container):
    from src.infrastructure.worker import Worker
    return Worker(container, delay=0.1)
