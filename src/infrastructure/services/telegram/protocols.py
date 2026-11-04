import datetime
from typing import Protocol, Optional


class StarGiftProtocol(Protocol):
    """Интерфейс для объекта StarGift из Telethon."""
    id: int
    title: Optional[str]
    stars: int
    availability_total: Optional[int]
    first_sale_date: Optional['datetime.datetime']
    limited: bool
    resell_min_stars: Optional[int]
    upgrade_stars: Optional[int]
