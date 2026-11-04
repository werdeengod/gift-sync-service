from typing import TYPE_CHECKING
import logging

from src.domain.ports import EventBusPort

if TYPE_CHECKING:
    from src.domain.events import DomainEvent
    from src.domain.ports.database.repositories import OutboxRepositoryPort

logger = logging.getLogger(__name__)


class OutboxEventPublisher(EventBusPort):
    def __init__(self, outbox_repo: 'OutboxRepositoryPort'):
        self.outbox_repo = outbox_repo

    async def publish(self, event: 'DomainEvent') -> None:
        await self.outbox_repo.save(event)
        logger.debug(f"Event saved in outbox: {event.event_type} (id={event.event_id})")
