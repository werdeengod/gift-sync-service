from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from src.domain.ports.dto import OutboxMessage


class MessageBrokerPort(ABC):
    @abstractmethod
    async def publish(self, message: 'OutboxMessage'):
        pass
