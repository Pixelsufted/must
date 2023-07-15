import socket
import threading
import com_base


class SocketServer(com_base.BaseServer):
    def __init__(self, app: any) -> None:
        super().__init__()
        self.app = app

    def destroy(self) -> None:
        self.app = None


class SocketClient(com_base.BaseClient):
    def __init__(self) -> None:
        super().__init__()
