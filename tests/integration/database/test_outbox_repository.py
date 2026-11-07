from typing import TYPE_CHECKING
import pytest

from src.domain.events import GiftCreated, EventStatus
from tests.factories import GiftFactory

if TYPE_CHECKING:
    from src.domain.ports.database.repositories import OutboxRepositoryPort
    from src.domain.ports.database import UoWPort


@pytest.mark.integration
async def test_save_event(uow: 'UoWPort', outbox_repository: 'OutboxRepositoryPort'):
    event = GiftCreated(gift=GiftFactory.create())

    async with uow.transaction():
        await outbox_repository.save(event)

    outbox_message = await outbox_repository.get_next_pending()
    assert outbox_message.event_id == event.event_id


@pytest.mark.integration
async def test_mark_event(uow: 'UoWPort', outbox_repository: 'OutboxRepositoryPort'):
    event = GiftCreated(gift=GiftFactory.create())

    async with uow.transaction():
        await outbox_repository.save(event)

    outbox_message1 = await outbox_repository.get_next_pending()
    await outbox_repository.mark_as(
        event_id=outbox_message1.event_id,
        status=EventStatus.SENT
    )

    outbox_message2 = await outbox_repository.get_next_pending()
    assert outbox_message2 is None

