from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from src.domain.entities import User


@dataclass(slots=True, frozen=True)
class UpdateGiftData:
    gift_id: int
    title: str
    user: 'User'

