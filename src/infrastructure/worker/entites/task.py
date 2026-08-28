from typing import Optional, Callable
from dataclasses import dataclass
import random


@dataclass
class Task:
    name: str
    handler: Callable
    workers: int = 1
    max_retries: int = 3
    retry_delay: float = 1.0
    max_retry_delay: float = 120.0
    timeout: Optional[float] = None
    fallback: Optional[Callable] = None

    def get_delay(self, attempt: int) -> float:
        base_delay = self.retry_delay * (2 ** attempt)
        capped = min(base_delay, self.max_retry_delay)
        return capped * (0.5 + random.uniform(0, 0.5))
