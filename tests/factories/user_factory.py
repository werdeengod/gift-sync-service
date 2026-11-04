from src.domain.entities import User


class UserFactory:
    @classmethod
    def create_admin_user(cls) -> User:
        return User(is_admin=True, user_id=1)

    @classmethod
    def create_user(cls) -> User:
        return User(is_admin=False, user_id=1)


