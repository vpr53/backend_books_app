import base64
from urllib.parse import unquote


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
            decoded_uid_str = unquote(uid_str)

            uid = int(base64.urlsafe_b64decode(decoded_uid_str.encode()).decode())
            return cls(uid)
        except Exception as e:
            raise ValueError("Неверный UID") from e

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
        return self._token == other

    def __repr__(self):
        return f"Token({self._token})"


# u_id = UserId(15)
# print(u_id.value)

# u_id = "MTE%3D"
# # u_id = u_id.encode()
# # print(u_id)

# print(UserId.decode(u_id).value)
