from abc import abstractmethod
from collections.abc import Iterator
from typing import Protocol

from app.kernel.model.id import Id


class Repository[NewModel, UpdateModel, Model](Protocol):
    @abstractmethod
    async def insert(self, source: NewModel) -> Model: ...

    @abstractmethod
    async def update(self, source: UpdateModel) -> Model: ...

    @abstractmethod
    async def get(self, source: Id) -> Model | None: ...

    @abstractmethod
    async def get_list(self, limit: int, offset: int) -> Iterator[Model]: ...

    @abstractmethod
    async def save(self) -> None: ...

    @abstractmethod
    async def delete(self, source: Id) -> Model: ...


class RepositoryRedis[NewModel, Model](Protocol):
    @abstractmethod
    async def read[_Key](self, source: _Key) -> Model | None: ...

    @abstractmethod
    async def write(self, source: NewModel) -> Model: ...

    @abstractmethod
    async def destroy[_Key](self, source: _Key) -> None: ...
