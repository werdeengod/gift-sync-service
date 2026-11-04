import json
from typing import TYPE_CHECKING
import pytest

from aio_pika import connect_robust, ExchangeType
from tests.factories import OutboxMessageFactory

if TYPE_CHECKING:
    from src.domain.ports.services import MessageBrokerPort


@pytest.mark.asyncio
async def test_publish(message_broker: 'MessageBrokerPort', rabbitmq_url):
    message = OutboxMessageFactory.create_outbox_message()
    await message_broker.publish(message)

    connection = await connect_robust(rabbitmq_url)
    async with connection:
        channel = await connection.channel()

        exchange = await channel.declare_exchange(
            "gift.events.topic",
            ExchangeType.TOPIC,
            durable=True,
        )

        queue = await channel.declare_queue(
            "test.gift.events.edited",
            durable=False,
            auto_delete=True,
        )
        await queue.bind(exchange, routing_key="gift.events.edited")

        await message_broker.publish(message)

        incoming = await queue.get(timeout=5)
        assert incoming is not None, "Сообщение не было отправлено"

        data = json.loads(incoming.body)
        assert data['event_id'] == str(message.event_id)
        assert incoming.routing_key == "gift.events.edited"

        await incoming.ack()
