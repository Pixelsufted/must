import socket
import threading
import com_base


class UDPServer(com_base.BaseServer):
    def __init__(self, app: any) -> None:
        super().__init__()
        self.should_kill = True
        self.app = app
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.sock.bind((app.config['socket_ip'], app.config['socket_port']))
        except OSError:
            raise RuntimeError('Failed to create socket')
        self.running = True
        self.buf_size = 1024 * 1024 * 100
        self.messages = {}
        threading.Thread(target=self.client_thread).start()

    def update(self) -> None:
        pass

    def client_thread(self) -> None:
        # TODO: multiple clients at the same time
        while self.running:
            try:
                encoded_msg, new_addr = self.sock.recvfrom(self.buf_size)
            except OSError:
                continue
            msg = self.decode_msg(encoded_msg)
            self.commands.append(msg)
        # self.should_kill = False

    def destroy(self) -> None:
        self.running = False
        if self.sock:
            self.sock.close()
            self.sock = None
        self.app = None


class UDPClient(com_base.BaseClient):
    def __init__(self, app: any) -> None:
        super().__init__(app)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_addr = (app.config['socket_ip'], app.config['socket_port'])

    def send(self, msg: str) -> None:
        if not msg or msg == 'i_want_to_live_please_do\'nt_die':
            return
        encoded_msg = com_base.BaseServer.encode_msg(msg)
        try:
            self.sock.sendto(encoded_msg, self.server_addr)
        except Exception as _err:
            raise RuntimeError(str(_err))

    def destroy(self) -> None:
        super().destroy()
        if self.sock:
            self.sock.close()
            self.sock = None
