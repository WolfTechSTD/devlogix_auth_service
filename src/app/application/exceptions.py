class UserException(Exception):
    pass


class UserExistsException(UserException):
    def __str__(self) -> str:
        return "Пользователь уже существует"


class UserNotFoundException(UserExistsException):
    def __str__(self) -> str:
        return "Пользователь не найден"


class UserLoginException(UserExistsException):
    def __str__(self) -> str:
        return "Данные введены неверно"


class UserWithUsernameExistsException(UserExistsException):
    def __str__(self) -> str:
        return "Пользователь с таким юзернейм уже существует"


class UserWithEmailExistsException(UserExistsException):
    def __str__(self) -> str:
        return "Пользователь с такой почтой уже существует"


class UserWithEmailAndUsernameExistsException(UserExistsException):
    def __str__(self) -> str:
        return "Пользователь с такими данными уже существует"


class InvalidTokenException(UserExistsException):
    def __str__(self) -> str:
        return "Доступ запрещен"
