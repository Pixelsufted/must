class BaseServer:
    def __init__(self) -> None:
        pass

    def update(self) -> None:
        pass

    def destroy(self) -> None:
        pass

    @staticmethod
    def encode_msg(msg: str) -> bytes:
        return msg.encode('utf-8', errors='replace')  # TODO: compress data maybe?

    @staticmethod
    def decode_msg(encoded_msg: bytes) -> str:
        return encoded_msg.decode('utf-8', errors='replace')


class BaseClient:
    def __init__(self, app: any) -> None:
        self.app = app

    def send(self, msg: str) -> None:
        pass

    def destroy(self) -> None:
        self.app = None
