from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from src.domain.events import DomainEvent


class EventBusPort(ABC):
    """Порт для отправки событий."""

    @abstractmethod
    async def publish(self, event: 'DomainEvent') -> None:
        pass
