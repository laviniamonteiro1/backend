import re
from blog.api.security import get_password_hash, verify_password


class PasswordValidationError(Exception):
    pass


class Password:
    def __init__(self, plain_password: str, hashed: bool = False):
        self._plain_password = plain_password
        if not hashed:
            self.validate(plain_password)
            self._hashed = get_password_hash(plain_password)
        else:
            self._hashed = plain_password

    def validate(self, password: str):
        if len(password) < 8:
            raise PasswordValidationError("A senha deve ter no mínimo 8 caracteres.")
        if not re.search(r"[A-Z]", password):
            raise PasswordValidationError(
                "A senha deve conter pelo menos uma letra maiúscula."
            )
        if not re.search(r"[a-z]", password):
            raise PasswordValidationError(
                "A senha deve conter pelo menos uma letra minúscula."
            )
        if not re.search(r"[0-9]", password):
            raise PasswordValidationError("A senha deve conter pelo menos um número.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise PasswordValidationError(
                "A senha deve conter pelo menos um caractere especial."
            )

    def verify(self, db: str) -> bool:
        return verify_password(self._plain_password, db)

    def __eq__(self, other) -> bool:
        return isinstance(other, Password) and self._hashed == other._hashed

    def __str__(self):
        return self._hashed
