from abc import abstractmethod
from typing import Protocol


class UoW(Protocol):
    @abstractmethod
    async def refresh(self): ...

    @abstractmethod
    async def commit(self): ...
