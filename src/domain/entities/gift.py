from typing import TYPE_CHECKING, Optional
from dataclasses import dataclass

if TYPE_CHECKING:
    import datetime
    from src.domain.value_objects import GiftTitle


@dataclass(slots=True)
class Gift:
    telegram_id: int
    stars: int
    date: Optional['datetime.datetime']
    availability_total: int
    title: 'GiftTitle'
    limited: bool
    is_upgradable: bool
