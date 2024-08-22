from typing import NewType

from ulid import ULID

Id = NewType("Id", ULID)
