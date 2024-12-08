class InvalidPasswordException(Exception):
    def __str__(self) -> str:
        return "Данные введены неверно"
