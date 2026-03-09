class UserAlreadyExistsError(Exception):
    """Ошибка возникает, если пользователь с таким email уже существует."""

    pass


class InvalidPasswordError(Exception):
    """Ошибка возникает, если пароль не соответствует требованиям безопасности."""

    pass


class EmailNotVerifiedError(Exception):
    """Ошибка возникает, если пользователь выполняет действие не подтвердив email"""

    pass


class UserNotFoundError(Exception):
    """Ошибка возникает, если пользователь не найден в репозитории."""

    pass


class InvalidTokenError(Exception):
    """Ошибка возникает, если пользователь предал неправильный токен"""

    pass
