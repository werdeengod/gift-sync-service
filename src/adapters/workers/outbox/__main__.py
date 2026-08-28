import asyncio
from dishka import FromDishka
from aiokafka import AIOKafkaProducer

from src.adapters.workers.args import ArgsParser
from src.bootstrap import build_container
from src.domain.events import EventStatus
from src.domain.entities import OutboxMessage
from src.domain.ports.database.repositories import OutboxRepositoryPort
from src.domain.ports.database import UoWPort
from src.infrastructure.serializers import JsonSerializer
from src.infrastructure.worker import Worker, WorkerRunner, Context

from .fallback import outbox_fallback

args = ArgsParser().get_args()
worker = Worker(build_container())


@worker.task(
    workers=args.workers,
    max_retries=args.retries,
    retry_delay=args.delay,
    timeout=args.timeout,
    fallback=outbox_fallback
)
async def outbox_processor(
        ctx: Context,
        outbox_repo: FromDishka[OutboxRepositoryPort],
        uow: FromDishka[UoWPort],
        outbox_serializer: FromDishka[JsonSerializer[OutboxMessage]],
        producer: FromDishka[AIOKafkaProducer]
):
    async with uow.transaction():
        ctx.message = await outbox_repo.get_next_pending()
        if not ctx.message:
            return

        message_json = outbox_serializer.to_json(ctx.message)

        await producer.send(
            topic="gifts.updated",
            value=message_json,
            key=str(ctx.message.event_id)
        )

        await outbox_repo.mark_as(
            event_id=ctx.message.event_id,
            status=EventStatus.SENT
        )


async def main():
    runner = WorkerRunner(worker)
    await runner.run()

if __name__ == '__main__':
    asyncio.run(main())
