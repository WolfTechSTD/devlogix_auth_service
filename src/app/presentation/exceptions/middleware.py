class UnauthorizedException(Exception):
    def __str__(self) -> str:
        return "Пользователь не авторизован"


class EmptyTokenException(Exception):
    def __str__(self) -> str:
        return "Доступ запрещен"
