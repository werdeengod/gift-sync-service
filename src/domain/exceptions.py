class DomainError(Exception):
    pass


class EntityNotFoundError(DomainError):
    def __init__(self, entity_type: str, entity_id: int):
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(f"{entity_type} with id {entity_id} not found")


class PermissionDeniedError(DomainError):
    def __init__(self, action: str, user_id: int):
        self.action = action
        self.user_id = user_id
        super().__init__(f"User {user_id} cannot perform {action}")


class ValidationError(DomainError):
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")