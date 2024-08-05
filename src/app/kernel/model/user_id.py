from typing import NewType

from ulid import ULID

UserId = NewType("UserId", ULID)
