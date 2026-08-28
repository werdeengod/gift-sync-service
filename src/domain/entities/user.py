from dataclasses import dataclass


@dataclass
class User:
    is_admin: bool
    user_id: int

