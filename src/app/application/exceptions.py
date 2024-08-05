class UserException(Exception):
    pass


class UserExistsException(UserException):
    def __str__(self) -> str:
        return "Пользователь уже существует"


class UserNotFoundException(UserExistsException):
    def __str__(self) -> str:
        return "Пользователь не найден"
