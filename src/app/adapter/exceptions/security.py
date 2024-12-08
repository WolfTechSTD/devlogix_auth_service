class ExpiredSignatureError(Exception):
    def __str__(self) -> str:
        return "Пользователь не авторизован"


class DecodeError(Exception):
    def __str__(self) -> str:
        return "Доступ запрещен"
