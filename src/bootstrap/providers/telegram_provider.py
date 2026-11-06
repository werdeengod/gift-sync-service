from contextlib import asynccontextmanager
from collections.abc import AsyncIterable
from dishka import Provider, Scope, provide, FromDishka
from telethon import TelegramClient
from telethon.sessions import StringSession

from src.domain.ports.services import TelegramGateway
from src.infrastructure.services.telegram import TelethonGateway, TelegramGiftMapper


class TelegramProvider(Provider):
    def __init__(self, session: str, api_id: int, api_hash: str):
        super().__init__()

        self.session = session
        self.api_id = api_id
        self.api_hash = api_hash

    @provide(scope=Scope.APP, provides=TelegramClient)
    @asynccontextmanager
    async def get_telegram_client(self) -> AsyncIterable[TelegramClient]:
        client = TelegramClient(
            session=StringSession(self.session),
            api_id=self.api_id,
            api_hash=self.api_hash
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
