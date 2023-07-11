import json
import os
import sys
import ctypes
import sdl2_backend


class App:
    def __init__(self, argv: any) -> None:
        self.exit_code = 1
        self.argv = argv
        self.is_le = sys.byteorder == 'little'
        self.cwd = os.path.dirname(__file__) or os.getcwd()
        self.paths = [self.cwd] + (os.getenv('LD_LIBRARY_PATH') or '').split(';') + (os.getenv('PATH') or '').split(';')
        self.encoding = 'utf-8'
        if sys.platform == 'win32':
            self.auto_prefix = ''
            self.load_library = ctypes.windll.LoadLibrary
        else:
            self.auto_prefix = 'lib'
            self.load_library = ctypes.CDLL
        self.config_path = os.path.join(self.cwd, 'config.json')
        if not os.path.isfile(self.config_path):
            self.write_json(
                os.path.join(self.cwd, 'config.json'), self.read_json(os.path.join(self.cwd, 'default_config.json'))
            )
        self.config = self.read_json(self.config_path)
        self.search_libs('libopusfile-0', 'libopus-0', 'libogg-0', 'libmodplug-1')
        self.bk = sdl2_backend.SDL2Backend(self, self.search_libs('SDL2', 'SDL2_mixer', prefix=self.auto_prefix))
        self.bk.init()
        self.bk.quit()
        self.bk.destroy()
        self.exit_code = 0

    def read_json(self, fp: str) -> dict:
        f = open(fp, 'r', encoding=self.encoding)
        content = f.read()
        f.close()
        return json.loads(content)

    def write_json(self, fp: str, content: dict) -> int:
        f = open(fp, 'w', encoding=self.encoding)
        result = f.write(json.dumps(content, indent=4))
        f.close()
        return result

    def stb(self, str_to_encode: str, encoding=None) -> bytes:
        return str_to_encode.encode(encoding or self.encoding, errors='replace')

    def bts(self, bytes_to_decode: bytes, encoding=None) -> str:
        return bytes_to_decode.decode(encoding or self.encoding, errors='replace')

    def search_libs(self, *libs: any, prefix: str = '') -> dict:
        result = {}
        for path in self.paths:
            for lib in libs:
                if result.get(lib):
                    continue
                try:
                    result[lib] = self.load_library(os.path.join(path, prefix + lib))
                except FileNotFoundError:
                    continue
        for lib in libs:
            if result.get(lib):
                continue
            try:
                result[lib] = self.load_library(prefix + lib)
            except FileNotFoundError:
                continue
        return result


if __name__ == '__main__':
    sys.exit(App(sys.argv).exit_code)
