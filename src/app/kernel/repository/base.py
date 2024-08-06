from abc import abstractmethod
from collections.abc import Iterator
from typing import Protocol, TypeVar

from app.kernel.model.id import Id

NewModel = TypeVar("NewModel")
Model = TypeVar("Model")


class Repository(Protocol[NewModel, Model]):
    @abstractmethod
    async def insert(self, source: NewModel) -> Model: ...

    @abstractmethod
    async def get(self, source: Id) -> Model | None: ...

    @abstractmethod
    async def get_list(self, limit: int, offset: int) -> Iterator[Model]: ...

    @abstractmethod
    async def save(self) -> None: ...

    @abstractmethod
    async def delete(self, source: Id) -> None: ...
