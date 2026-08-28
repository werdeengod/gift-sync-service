from typing import TYPE_CHECKING
from unittest.mock import call, ANY
import pytest

from tests.unit.factories import GiftFactory

if TYPE_CHECKING:
    from src.application.use_cases import SyncGiftsUseCase
    from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_initial_sync_when_db_empty(
    sync_gifts_use_case: 'SyncGiftsUseCase',
    mock_telegram_gateway: 'AsyncMock',
    mock_gift_repo: 'AsyncMock',
    mock_event_bus: 'AsyncMock',
    mock_uow: 'AsyncMock'
):
    external_gifts = GiftFactory.create_batch(3)
    mock_telegram_gateway.fetch_gifts.return_value = external_gifts
    mock_gift_repo.get_all.return_value = []

    await sync_gifts_use_case.execute()

    mock_gift_repo.save_all.assert_called_once_with(external_gifts)
    mock_uow.commit.assert_called_once()


@pytest.mark.asyncio
async def test_no_changes(
    sync_gifts_use_case: 'SyncGiftsUseCase',
    mock_telegram_gateway: 'AsyncMock',
    mock_gift_repo: 'AsyncMock',
    mock_event_bus: 'AsyncMock',
    mock_uow: 'AsyncMock'
):
    existing_gifts = GiftFactory.create_batch(2)
    external_gifts = GiftFactory.create_batch(2)

    mock_telegram_gateway.fetch_gifts.return_value = external_gifts
    mock_gift_repo.get_all.return_value = existing_gifts

    await sync_gifts_use_case.execute()

    mock_gift_repo.save_all.assert_not_called()
    mock_gift_repo.update.assert_not_called()
    mock_event_bus.publish.assert_not_called()
    mock_uow.commit.assert_not_called()


@pytest.mark.asyncio
async def test_with_upgradable_gifts(
    sync_gifts_use_case: 'SyncGiftsUseCase',
    mock_telegram_gateway: 'AsyncMock',
    mock_gift_repo: 'AsyncMock',
    mock_event_bus: 'AsyncMock',
    mock_uow: 'AsyncMock'
):
    existing_gifts = GiftFactory.create_batch(2)
    external_gifts = GiftFactory.create_batch_with_upgradable_gifts(2)

    mock_telegram_gateway.fetch_gifts.return_value = external_gifts
    mock_gift_repo.get_all.return_value = existing_gifts

    await sync_gifts_use_case.execute()

    mock_gift_repo.update.assert_has_calls([
        call(external_gifts[0]),
        call(external_gifts[1]),
    ])

    mock_event_bus.publish.assert_has_calls([
        call(ANY),
        call(ANY),
    ])

    mock_uow.commit.assert_called_once()


