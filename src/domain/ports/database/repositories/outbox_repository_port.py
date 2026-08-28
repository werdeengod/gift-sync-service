from typing import TYPE_CHECKING, Optional
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from uuid7 import UUID
    from src.domain.entities import OutboxMessage
    from src.domain.events import DomainEvent, EventStatus


class OutboxRepositoryPort(ABC):
    @abstractmethod
    async def save(self, event: 'DomainEvent') -> None:
        pass

    @abstractmethod
    async def get_next_pending(self) -> Optional['OutboxMessage']:
        pass

    @abstractmethod
    async def mark_as(self, event_id: 'UUID', status: 'EventStatus') -> None:
        pass
