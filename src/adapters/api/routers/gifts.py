from fastapi import APIRouter
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from src.application.dto import UpdateGiftData
from src.application.use_cases import UpdateGiftUseCase
from src.domain.ports.database.repositories import GiftRepositoryPort
from src.adapters.api.schemas.responses import GiftResponse
from src.adapters.api.schemas.requests import UpdateGiftRequest
from src.adapters.api.security import CurrentUser


router = APIRouter(
    prefix="/gifts",
    tags=["Gifts"],
    route_class=DishkaRoute
)


@router.get("/", response_model=list[GiftResponse])
async def get_all_gifts(repo: FromDishka[GiftRepositoryPort]):
    """Получить все подарки"""
    gifts = await repo.get_all()
    return [GiftResponse.from_domain(gift) for gift in gifts]


@router.patch("/{gift_id}", response_model=GiftResponse)
async def update_gift(
    gift_id: int,
    data: UpdateGiftRequest,
    user: CurrentUser,
    update_gift_use_case: FromDishka[UpdateGiftUseCase]
):
    """Обновить поля подарка"""
    dto = UpdateGiftData(gift_id=gift_id, title=data.title, user=user)
    gift = await update_gift_use_case.execute(dto)
    return GiftResponse.from_domain(gift)

