import re


class Email:
    def __init__(self, value: str):
        if not self._is_valid(value):
            raise ValueError("Invalid email address.")
        self._value = value

    def _is_valid(self, email: str) -> bool:
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    def value(self) -> str:
        return self._value

    def __eq__(self, other) -> bool:
        return isinstance(other, Email) and self._value == other._value

    def __str__(self) -> str:
        return self._value
