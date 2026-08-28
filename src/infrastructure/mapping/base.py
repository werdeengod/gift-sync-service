from abc import ABC, abstractmethod
from typing import TypeVar, Generic

DomainEntity = TypeVar('DomainEntity')
RawData = TypeVar('RawData')


class DataMapper(ABC, Generic[DomainEntity, RawData]):
    """Маппер данных в доменные сущности"""

    @abstractmethod
    def to_domain(self, model: RawData) -> DomainEntity:
        pass
