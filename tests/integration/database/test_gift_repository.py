from typing import TYPE_CHECKING
import pytest

from src.domain.exceptions import EntityNotFoundError
from src.domain.value_objects import GiftTitle
from tests.factories import GiftFactory

if TYPE_CHECKING:
    from src.domain.ports.database.repositories import GiftRepositoryPort
    from src.domain.ports.database import UoWPort


async def _create_gifts(uow: 'UoWPort', gift_repository: 'GiftRepositoryPort'):
    async with uow.transaction():
        gifts = GiftFactory.create_batch(2)
        await gift_repository.save_all(gifts)


@pytest.mark.asyncio
async def test_create_and_get_gift(uow: 'UoWPort', gift_repository: 'GiftRepositoryPort'):
    await _create_gifts(uow, gift_repository)
    gifts_from_db = await gift_repository.get_all()
    assert len(gifts_from_db) == 2


@pytest.mark.asyncio
async def test_update_gift(uow: 'UoWPort', gift_repository: 'GiftRepositoryPort'):
    await _create_gifts(uow, gift_repository)

    gift = await gift_repository.get(1)
    gift.title = GiftTitle(value="New Title")

    async with uow.transaction():
        await gift_repository.update(gift)

    updated_gift = await gift_repository.get(1)
    assert updated_gift.title.value == "New Title"


@pytest.mark.asyncio
async def test_patch_gift(uow: 'UoWPort', gift_repository: 'GiftRepositoryPort'):
    await _create_gifts(uow, gift_repository)

    async with uow.transaction():
        await gift_repository.patch(1, title="New gift")

    updated_gift = await gift_repository.get(1)
    assert updated_gift.title.value == "New gift"


@pytest.mark.asyncio
async def test_failed_patch_gift(uow: 'UoWPort', gift_repository: 'GiftRepositoryPort'):
    await _create_gifts(uow, gift_repository)

    with pytest.raises(EntityNotFoundError) as exc_info:
        async with uow.transaction():
            await gift_repository.patch(3, title="New gift")

        assert exc_info.value.entity_type == "Gift"
        assert exc_info.value.entity_id == 3
