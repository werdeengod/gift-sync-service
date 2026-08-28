from enum import StrEnum


class EventType(StrEnum):
    """Типы событий"""
    GIFT_UPGRADED = "gift.upgraded"
    GIFT_CREATED = "gift.created"


class EventStatus(StrEnum):
    """Статусы событий"""
    PENDING = "pending"
    PROCESSED = "processed"
    SENT = "sent"
    FAILED = "failed"
