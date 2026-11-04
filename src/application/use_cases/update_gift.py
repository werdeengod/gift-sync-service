from typing import TYPE_CHECKING
import logging

from src.domain.exceptions import PermissionDeniedError
from src.domain.value_objects import GiftTitle

if TYPE_CHECKING:
    from src.application.dto import UpdateGiftData
    from src.domain.ports.database.repositories import GiftRepositoryPort
    from src.domain.ports.database import UoWPort

logger = logging.getLogger(__name__)


class UpdateGiftUseCase:
    def __init__(
        self,
        gift_repo: 'GiftRepositoryPort',
        uow: 'UoWPort'
    ):
        self.gift_repo = gift_repo
        self.uow = uow

    async def execute(self, data: 'UpdateGiftData'):
        if not data.user.is_admin:
            raise PermissionDeniedError(
                action="gift_update",
                user_id=data.user.user_id
            )

        async with self.uow.transaction():
            validated_title = GiftTitle(data.title)

            gift = await self.gift_repo.patch(
                gift_id=data.gift_id,
                title=str(validated_title)
            )

        logger.info(
            f"Admin {data.user.user_id} updated the gift "
            f"(id={data.gift_id}) title to '{str(validated_title)}'"
        )

        return gift
