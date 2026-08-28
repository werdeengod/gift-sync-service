from typing import TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from src.domain.events import DomainEvent
    from src.domain.ports import EventBusPort
    from src.domain.ports.database.repositories import OutboxRepositoryPort

logger = logging.getLogger(__name__)


class EventBus(EventBusPort):
    def __init__(self, outbox_repo: 'OutboxRepositoryPort'):
        self.outbox_repo = outbox_repo

    async def publish(self, event: 'DomainEvent') -> None:
        logger.debug(f"Event saved in outbox: {event.event_type} (id={event.event_id})")
        await self.outbox_repo.save(event)
