class Interactor[InputView, OutputView]:
    async def __call__(self, data: InputView) -> OutputView:
        raise NotImplementedError(
            "The child class does not match the signature!"
        )
