from typing import Optional

from src.domain.events import DomainEvent
from src.domain.ports.dto import OutboxMessage
from src.domain.entities import Gift

from .base import Serializer


class GiftSerializer(Serializer[Gift]):
    def to_dict(self, entity: 'Gift') -> dict:
        return {
            "telegram_id": entity.telegram_id,
            "title": entity.title.value,
            "stars": entity.stars,
            "availability_total": entity.availability_total,
            "date": entity.date,
            "limited": entity.limited,
            "is_upgradable": entity.is_upgradable,
        }


class EventSerializer(Serializer[DomainEvent]):
    def __init__(self, gift_serializer: 'Serializer'):
        self.gift_serializer = gift_serializer

    def to_dict(self, entity: 'DomainEvent') -> dict:
        payload = self.gift_serializer.to_dict(entity.gift)

        return {
            "event_id": entity.event_id,
            "event_type": entity.event_type,
            "payload": self.gift_serializer.to_dict(entity.gift),
            "occurred_at": entity.occurred_at
        }


class OutboxMessageSerializer(Serializer[OutboxMessage]):
    def to_dict(self, entity: 'OutboxMessage') -> dict:
        return {
            "event_id": entity.event_id,
            "event_type": entity.event_type,
            "payload": entity.payload,
            "occurred_at": entity.occurred_at
        }
