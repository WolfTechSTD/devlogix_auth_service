from abc import abstractmethod, ABC


class BaseStrategy[Model](ABC):
    @abstractmethod
    async def read(self, source: Model) -> Model | None: ...

    @abstractmethod
    async def write(self, source: Model) -> Model: ...

    @abstractmethod
    async def destroy(self, source: Model) -> None: ...
