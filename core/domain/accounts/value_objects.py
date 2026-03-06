import base64

class UserId:
    def __init__(self, uid: int):
        if uid <= 0:
            raise ValueError("UID должен быть положительным")
        self._uid = uid

    @property
    def value(self) -> int:
        return self._uid

    def encode(self) -> str:
        return base64.urlsafe_b64encode(str(self._uid).encode()).decode()

    @classmethod
    def decode(cls, uid_str: str):
        try:
            uid = int(base64.urlsafe_b64decode(uid_str.encode()).decode())
            return cls(uid)
        except Exception:
            raise ValueError("Неверный UID")
    
    def __eq__(self, other):
        if not isinstance(other, UserId):
            return False
        return self._uid == other._uid

    def __repr__(self):
        return f"UserId({self._uid})"


class Token:
    def __init__(self, token: str):
        if not token:
            raise ValueError("Токен не может быть пустым")
        self._token = token

    @property
    def value(self) -> str:
        return self._token

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return self._token == other._token

    def __repr__(self):
        return f"Token({self._token})"
