from typing import TYPE_CHECKING
import logging

from src.domain.events import GiftUpgraded

if TYPE_CHECKING:
    from src.domain.ports import EventBusPort
    from src.domain.ports.services import TelegramGateway
    from src.domain.ports.database.repositories import GiftRepositoryPort
    from src.domain.ports.database import UoWPort


class SyncGiftsUseCase:
    def __init__(
            self,
            telegram_gateway: 'TelegramGateway',
            gift_repo: 'GiftRepositoryPort',
            uow: 'UoWPort',
            event_bus: 'EventBusPort'
    ):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.telegram_gateway = telegram_gateway
        self.gift_repo = gift_repo
        self.uow = uow
        self.event_bus = event_bus

    async def execute(self):
        # 1. Получаем данные
        external_gifts = await self.telegram_gateway.fetch_gifts()
        existing_gifts  = await self.gift_repo.get_all()

        # 2. Если в БД нет гифтов - сохраняем все
        if not existing_gifts:
            await self.gift_repo.save_all(external_gifts)
            await self.uow.commit()
            return

        # 3. Строим карты для быстрого поиска
        existing_map = {g.telegram_id: g for g in existing_gifts}
        external_map = {g.telegram_id: g for g in external_gifts}

        # 4. Определяем изменения
        created, updated, deleted  = [], [], []

        for external in external_gifts:
            existing = existing_map.get(external.telegram_id)

            if not existing:
                self.logger.info(f"[CREATED] New gift detected: {external}")
                created.append(external)
                continue

            if not existing.is_upgradable and external.is_upgradable:
                self.logger.info(f"[UPDATED] Updated gift detected: {external}")
                updated.append(external)

        for existing in existing_gifts:
            if existing.telegram_id not in external_map:
                deleted.append(existing.telegram_id)

        # 5. Применяем изменения
        if updated:
            async with self.uow.transaction():
                for gift in updated:
                    await self.gift_repo.update(gift)
                    await self.event_bus.publish(GiftUpgraded(gift=gift))

        if created:
            pass
