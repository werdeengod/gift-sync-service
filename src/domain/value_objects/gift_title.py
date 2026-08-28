from typing import Optional
from dataclasses import dataclass
from src.domain.exceptions import ValidationError


@dataclass(frozen=True)
class GiftTitle:
    value: Optional[str]

    def __post_init__(self):
        if not self.value:
            return

        if len(self.value) < 5:
            raise ValidationError("title", "must be at least 5 characters long")

        if len(self.value) > 100:
            raise ValidationError("title", "must be less than 100 characters")

        if not self.value.strip():
            raise ValidationError("title", "cannot be empty")

    def __str__(self) -> str:
        return self.value if self.value else "Untitled"

