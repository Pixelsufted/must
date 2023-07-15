class BaseServer:
    def __init__(self) -> None:
        pass

    def update(self) -> None:
        pass

    def destroy(self) -> None:
        pass


class BaseClient:
    def __init__(self, app: any) -> None:
        self.app = app

    def destroy(self) -> None:
        self.app = None
