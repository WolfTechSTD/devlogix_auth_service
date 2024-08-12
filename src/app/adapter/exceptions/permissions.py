class InvalidCookieTokenException(Exception):
    def __str__(self) -> str:
        return "Доступ запрещен"
