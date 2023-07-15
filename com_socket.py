import sys
import socket
import threading
import log
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
        self.clients = []
        self.sock.listen()
        self.running = True
        threading.Thread(target=self.accept_clients).start()

    def update(self) -> None:
        pass

    def accept_clients(self) -> None:
        while self.running and self.sock:
            try:
                conn, addr = self.sock.accept()
            except OSError:
                break
            self.clients.append(conn)
            threading.Thread(target=self.client_thread, args=(conn, addr)).start()

    def client_thread(self, conn: socket.socket, addr: tuple) -> None:
        should_exit = True
        while self.running:
            try:
                msg_len_buf = conn.recv(10)
                if not msg_len_buf:
                    continue
                msg_len = int.from_bytes(msg_len_buf, 'little', signed=False)
                encoded_msg = conn.recv(msg_len)
            except OSError:
                return
            msg = self.decode_msg(encoded_msg)
            log.info(msg)
            if msg == 'i_want_to_live_please_do\'nt_die':
                should_exit = False
            if should_exit:
                conn.close()
                self.clients.remove(conn)
                return
            if msg == 'disconnect':
                conn.close()
                self.clients.remove(conn)

    def destroy(self) -> None:
        for conn in self.clients:
            conn.close()
        self.clients.clear()
        self.running = False
        if self.sock:
            self.sock.close()
            self.sock = None
        self.app = None


class SocketClient(com_base.BaseClient):
    def __init__(self, app: any) -> None:
        super().__init__(app)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((app.config['socket_ip'], app.config['socket_port']))
        except Exception as _err:
            raise RuntimeError(str(_err))

    def send(self, msg: str) -> None:
        if not msg:
            return
        encoded_msg = com_base.BaseServer.encode_msg(msg)
        self.sock.send(int.to_bytes(len(encoded_msg), 10, 'little', signed=False) + encoded_msg)

    def destroy(self) -> None:
        super().destroy()
        if self.sock:
            self.sock.close()
            self.sock = None
