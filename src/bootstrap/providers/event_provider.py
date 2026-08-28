from aiokafka import AIOKafkaProducer
from dishka import Provider, Scope, provide, FromDishka
from contextlib import asynccontextmanager

from src.domain.ports import EventBusPort
from src.domain.ports.database.repositories import OutboxRepositoryPort
from src.infrastructure.event_bus import EventBus
from src.config import config


class EventProvider(Provider):
    @provide(scope=Scope.APP, provides=AIOKafkaProducer)
    @asynccontextmanager
    async def get_producer(self) -> AIOKafkaProducer:
        producer = AIOKafkaProducer(
            bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
            enable_idempotence=True,
        )

        await producer.start()

        try:
            yield producer
        finally:
            await producer.stop()

    @provide(scope=Scope.REQUEST, provides=EventBusPort)
    def get_event_bus(
            self,
            outbox_repo: FromDishka[OutboxRepositoryPort]
    ) -> EventBus:
        return EventBus(outbox_repo=outbox_repo)

