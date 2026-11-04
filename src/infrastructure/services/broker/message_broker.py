from typing import TYPE_CHECKING
from aio_pika import Message, DeliveryMode

from src.domain.ports.services import MessageBrokerPort

if TYPE_CHECKING:
    from aio_pika.abc import AbstractRobustConnection, AbstractExchange
    from src.infrastructure.serializers import JsonSerializer
    from src.domain.ports.dto import OutboxMessage


class AioPikaMessageBroker(MessageBrokerPort):
    def __init__(
        self,
        connection: 'AbstractRobustConnection',
        exchange: 'AbstractExchange',
        json_serializer: 'JsonSerializer[OutboxMessage]'
    ):
        self.connection = connection
        self.exchange = exchange
        self.json_serializer = json_serializer

    async def publish(self, outbox_message: 'OutboxMessage'):
        message = Message(
            body=self.json_serializer.to_json(outbox_message).encode('utf-8'),
            delivery_mode=DeliveryMode.PERSISTENT,
            content_type="application/json"
        )

        await self.exchange.publish(
            message=message,
            routing_key="gift.events.edited"
        )
