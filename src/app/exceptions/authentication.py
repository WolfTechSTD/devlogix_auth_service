class AuthenticationException(Exception):
    pass


class InvalidAuthenticationTokenError(AuthenticationException):
    def __str__(self) -> str:
        return "Доступ запрещен"
