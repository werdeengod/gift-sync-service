import pytest
from unittest.mock import AsyncMock
from contextlib import asynccontextmanager


@pytest.fixture
def mock_telegram_gateway():
    """Мок для TelegramGateway"""
    mock = AsyncMock()
    mock.fetch_gifts = AsyncMock()
    return mock


@pytest.fixture
def mock_gift_repo():
    """Мок для GiftRepositoryPort"""
    mock = AsyncMock()
    mock.get_all = AsyncMock()
    mock.save_all = AsyncMock()
    mock.update = AsyncMock()
    mock.update_from_dict = AsyncMock()

    return mock


@pytest.fixture
def mock_uow():
    """Мок для UoWPort"""
    mock = AsyncMock()

    mock.commit = AsyncMock()
    mock.begin = AsyncMock()
    mock.rollback = AsyncMock()

    @asynccontextmanager
    async def transaction():
        await mock.begin()
        try:
            yield mock
            await mock.commit()
        except Exception:
            await mock.rollback()
            raise

    mock.transaction = transaction

    return mock


@pytest.fixture
def mock_event_bus():
    """Мок для EventBusPort"""
    mock = AsyncMock()
    mock.publish = AsyncMock()
    return mock


@pytest.fixture
def sync_gifts_use_case(
    mock_telegram_gateway,
    mock_gift_repo,
    mock_uow,
    mock_event_bus
):
    from src.application.use_cases import SyncGiftsUseCase

    """Создает UseCase с моками"""
    return SyncGiftsUseCase(
        telegram_gateway=mock_telegram_gateway,
        gift_repo=mock_gift_repo,
        uow=mock_uow,
        event_bus=mock_event_bus
    )


@pytest.fixture
def update_gift_use_case(
    mock_telegram_gateway,
    mock_gift_repo,
    mock_uow,
    mock_event_bus
):
    from src.application.use_cases import UpdateGiftUseCase

    """Создает UseCase с моками"""
    return UpdateGiftUseCase(
        gift_repo=mock_gift_repo,
        uow=mock_uow
    )


