from typing import Protocol

from app.kernel.model.cookie_token import NewCookieToken, CookieToken
from .base import RepositoryRedis


class CookieTokenRepository(
    RepositoryRedis[NewCookieToken, CookieToken],
    Protocol
):
    pass
