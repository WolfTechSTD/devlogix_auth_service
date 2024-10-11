class UserException(Exception):
    pass


class UserExistsException(UserException):
    def __str__(self) -> str:
        return "Пользователь уже существует"


class UserLoginException(UserException):
    def __str__(self) -> str:
        return "Данные введены неверно"
