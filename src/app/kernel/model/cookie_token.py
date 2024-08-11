from dataclasses import dataclass


@dataclass
class CookieToken:
    key: str
    value: str


@dataclass
class NewCookieToken:
    key: str
    value: str
    lifetime_seconds: int
