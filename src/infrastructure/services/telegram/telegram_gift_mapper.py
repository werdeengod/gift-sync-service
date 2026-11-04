from src.infrastructure.mapping import DataMapper
from src.domain.entities import Gift
from src.domain.value_objects import GiftTitle
from .protocols import StarGiftProtocol


class TelegramGiftMapper(DataMapper[Gift, StarGiftProtocol]):
    def to_domain(self, model: 'StarGiftProtocol') -> 'Gift':
        return Gift(
            stars=model.stars,
            date=model.first_sale_date,
            title=GiftTitle(model.title),
            telegram_id=model.id,
            availability_total=model.availability_total,
            is_upgradable=model.upgrade_stars is not None and model.resell_min_stars is None,
            limited=model.limited
        )
