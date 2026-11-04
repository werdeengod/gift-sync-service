from typing import TYPE_CHECKING
import pytest

from src.application.dto import UpdateGiftData
from src.domain.exceptions import PermissionDeniedError, ValidationError
from tests.factories import UserFactory

if TYPE_CHECKING:
    from src.application.use_cases import UpdateGiftUseCase
    from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_permission_denied(update_gift_use_case: 'UpdateGiftUseCase'):
    data = UpdateGiftData(gift_id=1, title='123', user=UserFactory.create_user())

    with pytest.raises(PermissionDeniedError) as exc_info:
        await update_gift_use_case.execute(data)

    assert exc_info.value.action == "gift_update"
    assert exc_info.value.user_id == data.user.user_id


@pytest.mark.asyncio
async def test_update_gift(
    update_gift_use_case: 'UpdateGiftUseCase',
    mock_gift_repo: 'AsyncMock',
    mock_uow: 'AsyncMock'
):
    data = UpdateGiftData(gift_id=1, title='Test Title', user=UserFactory.create_admin_user())

    await update_gift_use_case.execute(data)

    mock_gift_repo.update_from_dict.assert_called_once_with(
        gift_id=data.gift_id,
        title=data.title
    )
    mock_uow.commit.assert_called_once()


@pytest.mark.asyncio
async def test_invalid_title_for_gift(update_gift_use_case: 'UpdateGiftUseCase'):
    data = UpdateGiftData(gift_id=1, title='T', user=UserFactory.create_admin_user())

    with pytest.raises(ValidationError) as exc_info:
        await update_gift_use_case.execute(data)

    assert exc_info.value.field == "title"







