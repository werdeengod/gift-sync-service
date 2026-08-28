from typing import TYPE_CHECKING, Optional
from datetime import datetime

from sqlalchemy import insert, update, select

from src.domain.events import EventStatus
from src.domain.ports.database.repositories import OutboxRepositoryPort
from src.infrastructure.database.models import Outbox

if TYPE_CHECKING:
    from uuid7 import UUID
    from sqlalchemy.ext.asyncio import AsyncSession
    from src.infrastructure.serializers import Serializer
    from src.infrastructure.mapping import DataMapper
    from src.domain.entities import OutboxMessage
    from src.domain.events import DomainEvent


class OutboxRepository(OutboxRepositoryPort):
    def __init__(
            self,
            session: 'AsyncSession',
            outbox_mapper: 'DataMapper',
            event_serializer: 'Serializer'
    ):
        self.session = session
        self.outbox_mapper = outbox_mapper
        self.event_serializer = event_serializer

    async def save(self, event: 'DomainEvent') -> None:
        stmt = insert(Outbox).values(**self.event_serializer.to_dict(event))
        await self.session.execute(stmt)

    async def get_next_pending(self) -> Optional['OutboxMessage']:
        result = await self.session.execute(
            select(Outbox)
            .where(Outbox.status == EventStatus.PENDING)
            .with_for_update(skip_locked=True)
        )

        message = result.scalars().first()

        if not message:
            return

        return self.outbox_mapper.to_domain(message)

    async def mark_as(self, event_id: 'UUID', status: 'EventStatus') -> None:
        sent_at = datetime.now() if status == EventStatus.SENT else None

        await self.session.execute(
            update(Outbox)
            .where(Outbox.event_id == event_id)
            .values(status=status, sent_at=sent_at)
        )
