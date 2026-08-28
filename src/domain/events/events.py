from .event_type import EventType
from .base import DomainEvent


class GiftUpgraded(DomainEvent):
    @property
    def event_type(self) -> 'EventType':
        return EventType.GIFT_UPGRADED


class GiftCreated(DomainEvent):
    @property
    def event_type(self) -> 'EventType':
        return EventType.GIFT_CREATED
