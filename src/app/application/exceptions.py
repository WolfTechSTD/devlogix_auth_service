class UserException(Exception):
    pass


class UserExistsException(UserException):
    def __str__(self) -> str:
        return "Пользователь уже существует"
