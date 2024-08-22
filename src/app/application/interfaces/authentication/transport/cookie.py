from abc import abstractmethod, ABC


class ACookieTransport(ABC):
    @abstractmethod
    def set_login_cookie[Response](self,response: Response) -> Response: ...

    @abstractmethod
    def set_logout_cookie[Response](self, response: Response) -> Response: ...
