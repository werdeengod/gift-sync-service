from src.infrastructure.database.models import Outbox
from src.infrastructure.mapping import DataMapper
from src.domain.entities import OutboxMessage


class OutboxMapper(DataMapper[OutboxMessage, Outbox]):
    def to_domain(self, model: 'Outbox') -> 'OutboxMessage':
        return OutboxMessage(
            event_id=model.event_id,
            event_type=model.event_type,
            occurred_at=model.occurred_at,
            payload=model.payload,
            sent_at=model.sent_at,
            status=model.status
        )
