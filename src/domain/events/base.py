from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from datetime import datetime
import uuid7

if TYPE_CHECKING:
    from .event_type import EventType
    from src.domain.entities import Gift


class DomainEvent(ABC):
    def __init__(self, gift: 'Gift'):
        self.event_id = uuid7.create()
        self.occurred_at = datetime.now()
        self.gift = gift

    @property
    @abstractmethod
    def event_type(self) -> 'EventType':
        pass
