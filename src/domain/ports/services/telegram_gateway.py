from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from src.domain.entities import Gift


class TelegramGateway(ABC):
    @abstractmethod
    async def fetch_gifts(self) -> list['Gift']:
        pass
