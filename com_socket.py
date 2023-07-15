import asyncio
import socket
import threading
import com_base


class SocketServer(com_base.BaseServer):
    def __init__(self, app: any) -> None:
        super().__init__()
        self.app = app
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.bind((app.config['socket_ip'], app.config['socket_port']))
        except OSError:
            raise RuntimeError('Failed to create socket')
        # self.sock.setblocking(False)
        self.sock.listen()
        self.running = True
        threading.Thread(target=self.accept_clients).start()

    def accept_clients(self) -> None:
        while self.running:
            conn, addr = self.sock.accept()
            print(conn, addr)

    def destroy(self) -> None:
        self.running = False
        if self.sock:
            self.sock.close()
            self.sock = None
        self.app = None


class SocketClient(com_base.BaseClient):
    def __init__(self) -> None:
        super().__init__()
