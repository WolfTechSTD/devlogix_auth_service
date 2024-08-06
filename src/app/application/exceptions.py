class UserException(Exception):
    pass


class UserExistsException(UserException):
    def __str__(self) -> str:
        return "Пользователь уже существует"


class UserNotFoundException(UserExistsException):
    def __str__(self) -> str:
        return "Пользователь не найден"


class UserWithUsernameExistsException(UserExistsException):
    def __str__(self) -> str:
        return "Пользователь с таким юзернейм уже существует"


class UserWithEmailExistsException(UserExistsException):
    def __str__(self) -> str:
        return "Пользователь с такой почтой уже существует"
