import datetime

from pydantic import BaseModel
from src.domain.entities import Gift


class GiftResponse(BaseModel):
    telegram_id: str
    name: str
    is_upgradable: bool
    is_upgraded: bool
    date: datetime.datetime
    availability_total: int
    stars: int
    limited: bool

    @classmethod
    def from_domain(cls, gift: 'Gift') -> 'GiftResponse':
        return cls(
            telegram_id=gift.telegram_id,
            name=str(gift.title),
            is_upgradable=gift.is_upgradable,
            date=gift.date,
            availability_total=gift.availability_total,
            stars=gift.stars,
            limited=gift.limited
        )
