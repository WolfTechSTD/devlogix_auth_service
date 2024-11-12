from abc import abstractmethod, ABC


class ICookieTransport(ABC):
    @abstractmethod
    def set_login_cookie[Response](
            self,
            response: Response,
            access_token: str,
            access_token_time: int,
            refresh_token: str,
            refresh_token_time: int,
    ) -> Response: ...

    @abstractmethod
    def set_logout_cookie[Response](self, response: Response) -> Response: ...

    @abstractmethod
    def update_access_token[Response](
            self,
            response: Response,
            access_token: str,
            access_token_time: int
    ) -> Response: ...
