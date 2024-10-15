class UserException(Exception):
    pass


class UserLoginException(UserException):
    def __str__(self) -> str:
        return "Данные введены неверно"
