class MockTransaction:
    def __init__(self) -> None:
        self.is_committed = False
        self.is_rollback = False

    async def commit(self) -> None:
        self.is_committed = True

    async def rollback(self) -> None:
        self.is_rollback = True
