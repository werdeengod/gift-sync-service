import json
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from .encoder import JSONEncoder

DomainObject = TypeVar('DomainObject')


class Serializer(ABC, Generic[DomainObject]):
    """Контракт для преобразования доменного объекта в словарь."""

    @abstractmethod
    def to_dict(self, entity: DomainObject) -> dict:
        pass


class JsonSerializer(Generic[DomainObject]):
    """Декоратор для преобразования доменного объекта в JSON."""

    def __init__(self, base_serializer: 'Serializer[DomainObject]'):
        self.base_serializer = base_serializer

    def to_json(self, entity: DomainObject) -> str:
        data = self.base_serializer.to_dict(entity)
        return json.dumps(data, cls=JSONEncoder, default=str)
