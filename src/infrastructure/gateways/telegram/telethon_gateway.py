from typing import TYPE_CHECKING

from telethon import TelegramClient
from telethon.tl import functions

from src.domain.ports.services import TelegramGateway

if TYPE_CHECKING:
    from telethon.tl.types.payments import StarGifts
    from src.domain.entities import Gift
    from src.infrastructure.mapping import DataMapper


class TelethonGateway(TelegramGateway):
    def __init__(self, client: 'TelegramClient', telegram_gift_mapper: 'DataMapper'):
        self.client = client
        self.telegram_gift_mapper = telegram_gift_mapper

    async def fetch_gifts(self) -> list['Gift']:
        result: 'StarGifts' = await self.client(functions.payments.GetStarGiftsRequest(hash=0))

        return [
            self.telegram_gift_mapper.to_domain(telegram_gift)
            for telegram_gift in result.gifts
        ]
