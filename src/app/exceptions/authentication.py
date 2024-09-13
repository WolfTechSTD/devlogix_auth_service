class AuthenticationException(Exception):
    pass


class InvalidAuthenticationTokenError(AuthenticationException):
    def __str__(self) -> str:
        return "Доступ запрещен"


class UserAuthException(AuthenticationException):
    def __str__(self) -> str:
        return "Пользователь авторизован"
