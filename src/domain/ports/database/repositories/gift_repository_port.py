from typing import TYPE_CHECKING, Optional
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from src.domain.entities import Gift


class GiftRepositoryPort(ABC):
    @abstractmethod
    async def get(self, gift_id: int) -> Optional['Gift']:
        pass

    @abstractmethod
    async def get_all(self) -> Optional[list['Gift']]:
        pass

    @abstractmethod
    async def save_all(self, gifts: list['Gift']) -> None:
        pass

    @abstractmethod
    async def update(self, gift: 'Gift') -> Optional['Gift']:
        pass

    @abstractmethod
    async def patch(self, gift_id: int, **kwargs: dict) -> Optional['Gift']:
        pass
