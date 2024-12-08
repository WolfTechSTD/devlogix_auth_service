class InvalidEmailOrUsername(Exception):
    def __str__(self) -> str:
        return "Данные введены неверно"


class InvalidTokenException(Exception):
    def __str__(self) -> str:
        return "Доступ запрещен"
