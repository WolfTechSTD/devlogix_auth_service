from dataclasses import dataclass, field
import datetime as dt


@dataclass(slots=True, kw_only=True)
class RedisToken:
    key: str
    value: str | None = field(default=None)
    lifetime_second: int | dt.timedelta | None = field(default=None)


@dataclass(slots=True)
class AccessToken:
    value: str
