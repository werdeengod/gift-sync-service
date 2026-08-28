import json
from datetime import datetime, date
from enum import Enum
from uuid7 import UUID


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()

        if isinstance(obj, date):
            return obj.isoformat()

        if isinstance(obj, UUID):
            return str(obj)

        if isinstance(obj, Enum):
            return obj.value

        return super().default(obj)
