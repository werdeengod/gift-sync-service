from typing import TYPE_CHECKING, Optional
from sqlalchemy import select, insert, update

from src.infrastructure.database.models import Gift as GiftORM
from src.domain.ports.database.repositories import GiftRepositoryPort
from src.domain.exceptions import EntityNotFoundError

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from src.domain.entities import Gift
    from src.infrastructure.mapping import DataMapper
    from src.infrastructure.serializers import Serializer


class GiftRepository(GiftRepositoryPort):
    def __init__(
            self,
            session: 'AsyncSession',
            gift_mapper: 'DataMapper',
            gift_serializer: 'Serializer'
    ):
        self.session = session
        self.gift_mapper = gift_mapper
        self.gift_serializer = gift_serializer

    async def get(self, gift_id: int) -> Optional['Gift']:
        stmt = (
            select(GiftORM)
            .where(GiftORM.telegram_id == gift_id)
        )

        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if not model:
            return None

        return self.gift_mapper.to_domain(model)

    async def get_all(self) -> Optional[list['Gift']]:
        result = await self.session.execute(select(GiftORM))
        models = result.scalars().all()

        if not models:
            return None

        return [self.gift_mapper.to_domain(model) for model in models]

    async def save_all(self, gifts: list['Gift']) -> None:
        values = [self.gift_serializer.to_dict(gift) for gift in gifts]
        await self.session.execute(insert(GiftORM).values(values))

    async def update(self, gift: 'Gift') -> None:
        stmt = (
            update(GiftORM)
            .where(GiftORM.telegram_id == gift.telegram_id)
            .values(**self.gift_serializer.to_dict(gift))
        )
        await self.session.execute(stmt)

    async def patch(self, gift_id: int, **kwargs) -> Optional['Gift']:
        stmt = (
            update(GiftORM)
            .where(GiftORM.telegram_id == gift_id)
            .values(kwargs)
            .returning(GiftORM)
        )

        result = await self.session.execute(stmt)
        updated_gift = result.scalar_one_or_none()

        if not updated_gift:
            raise EntityNotFoundError(
                entity_type='Gift',
                entity_id=gift_id
            )

        return self.gift_mapper.to_domain(updated_gift)
