from abc import abstractmethod
from typing import Protocol


class Transaction(
    Protocol
):
    @abstractmethod
    async def rollback(
            self
    ) -> None: ...

    @abstractmethod
    async def commit(
            self
    ) -> None: ...
