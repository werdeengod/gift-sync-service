import json
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from .encoder import json_serializer

DomainObject = TypeVar('DomainObject')


class Serializer(ABC, Generic[DomainObject]):
    """Контракт для преобразования объекта в словарь."""

    @abstractmethod
    def to_dict(self, entity: DomainObject) -> dict:
        pass


class JsonSerializer(Generic[DomainObject]):
    """Декоратор для преобразования объекта в JSON."""

    def __init__(self, base_serializer: 'Serializer[DomainObject]'):
        self.base_serializer = base_serializer

    def to_json(self, entity: DomainObject) -> str:
        data = self.base_serializer.to_dict(entity)
        return json_serializer(data)
