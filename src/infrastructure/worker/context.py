from typing import Optional, Any


class Context:
    def __init__(self):
        self._data = {}
        self.errors = []

    def __getitem__(self, key: str):
        return self.get(key)

    def __setitem__(self, key: str, value: Any):
        self._data[key] = value

    def add_error(self, error: Exception) -> None:
        self.errors.append(error)

    def get(self, key: str) -> Any:
        return self._data[key]

    def get_last_error(self) -> Optional[Exception]:
        return self.errors[-1] if self.errors else None

    def get_data(self) -> dict:
        return self._data
