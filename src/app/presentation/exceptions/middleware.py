class AuthorizedException(Exception):
    def __str__(self) -> str:
        return "Пользователь авторизован"


class EmptyTokenException(Exception):
    def __str__(self) -> str:
        return "Доступ запрещен"
