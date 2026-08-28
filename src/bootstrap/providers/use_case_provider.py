from dishka import Provider, Scope, provide, FromDishka
from telethon import TelegramClient

from src.application.use_cases import UpdateGiftUseCase, SyncGiftsUseCase
from src.domain.ports.database import UoWPort
from src.domain.ports.database.repositories import GiftRepositoryPort
from src.domain.ports import EventBusPort


class UseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=UpdateGiftUseCase)
    async def get_update_gift(
        self,
        gift_repo: FromDishka[GiftRepositoryPort],
        uow: FromDishka[UoWPort],
    ):
        return UpdateGiftUseCase(
            gift_repo=gift_repo,
            uow=uow,
        )

    @provide(scope=Scope.REQUEST, provides=SyncGiftsUseCase)
    async def get_sync_gifts(
        self,
        telegram_gateway: FromDishka[TelegramClient],
        gift_repo: FromDishka[GiftRepositoryPort],
        uow: FromDishka[UoWPort],
        event_bus: FromDishka[EventBusPort]
    ):
        return SyncGiftsUseCase(
            telegram_gateway=telegram_gateway,
            gift_repo=gift_repo,
            uow=uow,
            event_bus=event_bus
        )
