import datetime

from src.domain.value_objects import GiftTitle
from src.domain.entities import Gift


class GiftFactory:
    @classmethod
    def create_batch(cls, amount: int):
        return [
            Gift(
                telegram_id=telegram_id,
                date=datetime.datetime(2026, 1, 1),
                availability_total=100,
                title=GiftTitle("Test gift"),
                is_upgradable=False,
                limited=True,
                stars=100
            )
            for telegram_id in range(1, amount + 1)
        ]

    @classmethod
    def create_batch_with_upgradable_gifts(cls, amount: int):
        return [
            Gift(
                telegram_id=telegram_id,
                date=None,
                availability_total=10000,
                title=GiftTitle("New gift"),
                is_upgradable=True,
                limited=True,
                stars=100
            )
            for telegram_id in range(1, amount + 1)
        ]

    @classmethod
    def create(cls) -> 'Gift':
        return Gift(
            telegram_id=1,
            date=datetime.datetime(2026, 1, 1),
            availability_total=100,
            title=GiftTitle("Test gift"),
            is_upgradable=False,
            limited=True,
            stars=100
        )
