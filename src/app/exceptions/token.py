class TokenException(Exception):
    pass


class InvalidTokenException(TokenException):
    def __str__(self) -> str:
        return "Доступ запрещен"


class TokenTimeException(TokenException):
    def __str__(self) -> str:
        return "Пользователь на авторизован"
