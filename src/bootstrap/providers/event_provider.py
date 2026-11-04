from typing import Optional
from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide, FromDishka
from aio_pika import connect_robust, ExchangeType
from aio_pika.abc import AbstractRobustConnection, AbstractExchange

from src.domain.ports import EventBusPort
from src.domain.ports.dto import OutboxMessage
from src.domain.ports.services import MessageBrokerPort
from src.domain.ports.database.repositories import OutboxRepositoryPort
from src.infrastructure.serializers import JsonSerializer
from src.infrastructure.event_bus import OutboxEventPublisher
from src.infrastructure.services.broker import AioPikaMessageBroker


class EventProvider(Provider):
    def __init__(self, broker_url: Optional[str] = None):
        super().__init__()
        self.broker_url = broker_url

    @provide(scope=Scope.APP)
    async def get_broker_connection(self) -> AsyncIterable[AbstractRobustConnection]:
        connection = await connect_robust(self.broker_url)
        await connection.connect()

        try:
            yield connection
        finally:
            await connection.close()

    @provide(scope=Scope.APP)
    async def get_exchange(self, connection: AbstractRobustConnection) -> AbstractExchange:
        channel = await connection.channel()

        return await channel.declare_exchange(
            "gift.events.topic",
            ExchangeType.TOPIC,
            durable=True,
        )

    @provide(scope=Scope.APP, provides=MessageBrokerPort)
    async def get_message_broker(
        self,
        connection: AbstractRobustConnection,
        exchange: AbstractExchange,
        json_serializer: JsonSerializer[OutboxMessage]
    ) -> MessageBrokerPort:
        return AioPikaMessageBroker(connection, exchange, json_serializer)

    # @provide(scope=Scope.REQUEST, provides=EventBusPort)
    # def get_event_bus(
    #         self,
    #         outbox_repo: FromDishka[OutboxRepositoryPort]
    # ) -> OutboxEventPublisher:
    #     return OutboxEventPublisher(outbox_repo=outbox_repo)

