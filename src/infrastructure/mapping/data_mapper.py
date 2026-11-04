from abc import ABC, abstractmethod
from typing import TypeVar, Generic

Target = TypeVar('Target')
RawData = TypeVar('RawData')


class DataMapper(ABC, Generic[Target, RawData]):
    """Маппер сырых данных в целевой тип (доменную сущность или DTO)"""

    @abstractmethod
    def to_domain(self, model: RawData) -> Target:
        pass
