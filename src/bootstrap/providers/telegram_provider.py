from contextlib import asynccontextmanager
from collections.abc import AsyncIterable
from dishka import Provider, Scope, provide, FromDishka
from telethon import TelegramClient

from src.domain.ports.services import TelegramGateway
from src.infrastructure.services.telegram import TelethonGateway, TelegramGiftMapper
from src.config import config


class TelegramProvider(Provider):
    @provide(scope=Scope.APP, provides=TelegramClient)
    @asynccontextmanager
    async def get_telegram_client(self) -> AsyncIterable[TelegramClient]:
        client = TelegramClient(
            session=config.TELEGRAM_SESSION_NAME,
            api_id=config.TELEGRAM_API_ID,
            api_hash=config.TELEGRAM_API_HASH,
        )

        async with client:
            yield client

    @provide(scope=Scope.APP)
    def get_telegram_gift_mapper(self) -> TelegramGiftMapper:
        return TelegramGiftMapper()

    @provide(scope=Scope.APP, provides=TelegramGateway)
    async def get_telegram_gateway(
        self,
        client: FromDishka[TelegramClient],
        mapper: FromDishka[TelegramGiftMapper]
    ) -> TelethonGateway:
        return TelethonGateway(client, mapper)
