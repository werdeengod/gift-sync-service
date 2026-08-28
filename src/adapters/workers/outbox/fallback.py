from typing import Optional
from dishka import FromDishka
from sqlalchemy.exc import TimeoutError as DatabaseTimeoutError

from src.domain.events import EventStatus
from src.domain.entities import OutboxMessage
from src.domain.ports.database.repositories import OutboxRepositoryPort
from src.domain.ports.database import UoWPort
from src.infrastructure.worker.entites import Context


async def outbox_fallback(
        ctx: Context,
        outbox_repo: FromDishka[OutboxRepositoryPort],
        uow: FromDishka[UoWPort],
):
    message: Optional['OutboxMessage'] = ctx.get('message')
    last_error = ctx.get_last_error()

    if not message:
        return

    if isinstance(last_error, DatabaseTimeoutError):
        # TODO: реализовать запись на диск при недоступности к БД
        return

    async with uow.transaction():
        await outbox_repo.mark_as(
            event_id=message.event_id,
            status=EventStatus.FAILED
        )
