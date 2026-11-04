import datetime
import uuid7

from src.domain.events import EventType, EventStatus
from src.domain.ports.dto import OutboxMessage


class OutboxMessageFactory:
    @classmethod
    def create_outbox_message(cls) -> OutboxMessage:
        return OutboxMessage(
            event_id=uuid7.create(),
            event_type=EventType.GIFT_CREATED,
            occurred_at=datetime.datetime.now(),
            payload={"test": 123},
            sent_at=datetime.datetime.now(),
            status=EventStatus.SENT
        )

