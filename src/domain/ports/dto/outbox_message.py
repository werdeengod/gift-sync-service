from typing import TYPE_CHECKING, Optional
from dataclasses import dataclass

from src.domain.events import EventType, EventStatus

if TYPE_CHECKING:
    import datetime
    from uuid7 import UUID


@dataclass
class OutboxMessage:
    event_id: 'UUID'
    event_type: 'EventType'
    occurred_at: 'datetime.datetime'
    payload: dict
    sent_at: Optional['datetime.datetime']
    status: 'EventStatus'
