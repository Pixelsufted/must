import os
import sys
import json
import random
import ctypes
import log
import com_base
import com_socket
import backend_base
import backend_sdl2
import backend_fmodex


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
        if self.config['com_type'] == 'tcp':
            self.server = com_socket.SocketServer(self)
        else:
            raise RuntimeError('Unknown communication type')
        if self.config['audio_backend'] == 'sdl2':
            self.search_libs('libopusfile-0', 'libopus-0', 'libogg-0', 'libmodplug-1')
            self.bk: backend_base.BaseBackend = backend_sdl2.SDL2Backend(
                self, self.search_libs('SDL2', 'SDL2_mixer', prefix=self.auto_prefix)
            )
        elif self.config['audio_backend'] == 'fmodex':
            if sys.platform == 'win32':
                self.search_libs('VCRUNTIME140_APP')
            self.search_libs('libfsbvorbis64')
            self.bk: backend_base.BaseBackend = backend_fmodex.FmodExBackend(
                self, self.search_libs('opus', 'media_foundation', 'fsbank', 'fmod', prefix=self.auto_prefix)
            )
        else:
            raise RuntimeError('Unknown audio backend')
        self.bk.init()
        self.volume = self.config['volume']
        if self.volume > 1.0:
            raise RuntimeError(f'Volume {self.volume} is bigger than 1.0')
        self.full_list = []
        for arg in self.argv[1:]:
            ext = arg.split('.')[-1].lower()
            if ext not in self.config['formats']:
                continue
            self.full_list.append(arg)
        if not self.full_list and self.config['music_path']:
            for fn in os.listdir(self.config['music_path']):
                ext = fn.split('.')[-1].lower()
                if ext not in self.config['formats']:
                    continue
                self.full_list.append(os.path.join(self.config['music_path'], fn))
        self.current_music: base_backend.BaseMusic = None # noqa
        if os.getenv('TEST_MUSIC'):
            self.mus = self.bk.open_music('E:\\Music\\Mittsies - Vitality (V3 Remix).mp3')
            self.mus.play()
            self.mus.set_volume(self.volume)
            while self.mus.is_playing():
                self.bk.update()
            self.mus.destroy()
            self.cleanup()
            self.bk.quit()
            self.bk.destroy()
            self.exit_code = 0
            return
        self.running = True
        self.default_track_id = -1
        self.main_loop()
        self.cleanup()
        self.bk.quit()
        self.bk.destroy()
        self.exit_code = 0

    def track_loop(self) -> None:
        while self.running and self.current_music and self.current_music.is_playing():
            self.bk.update()

    def next_track(self) -> any:
        # TODO: maybe allow to change mode in real time?
        if self.config['main_playlist_mode'] == 'default':
            self.default_track_id += 1
            if self.default_track_id >= len(self.full_list):
                self.default_track_id = 0
            fp = self.full_list[self.default_track_id]
            try:
                return self.bk.open_music(fp)
            except RuntimeError:
                return None
        elif self.config['main_playlist_mode'] == 'full_random':
            fp = random.choice(self.full_list)
            try:
                return self.bk.open_music(fp)
            except RuntimeError:
                return None
        return None

    def main_loop(self) -> None:
        while self.running:
            mus: backend_base.BaseMusic = self.next_track()
            while not mus:
                mus = self.next_track()
            log.info(mus.fn)
            self.play_new_music(mus)
            self.track_loop()

    def play_new_music(self, mus: backend_base.BaseMusic) -> None:
        if self.current_music:
            self.current_music.stop()
            self.current_music.destroy()
        mus.play()
        mus.set_volume(self.volume)
        self.current_music = mus

    def cleanup(self) -> None:
        if self.current_music:
            self.current_music.stop()
            self.current_music.destroy()
            self.current_music = None

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
