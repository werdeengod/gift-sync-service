from src.infrastructure.database.models import Gift as GiftORM
from src.infrastructure.mapping import DataMapper
from src.domain.entities import Gift
from src.domain.value_objects import GiftTitle


class GiftMapper(DataMapper[Gift, GiftORM]):
    def to_domain(self, model: 'GiftORM') -> 'Gift':
        return Gift(
            stars=model.stars,
            date=model.date,
            title=GiftTitle(value=model.title),
            telegram_id=model.telegram_id,
            availability_total=model.availability_total,
            limited=model.limited,
            is_upgradable=model.is_upgradable
        )
