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
        self.first_arg = argv[0]
        self.argv = argv[1:]
        self.is_le = sys.byteorder == 'little'
        self.cwd = os.path.dirname(__file__) or os.getcwd()
        self.paths = [self.cwd] + (os.getenv('LD_LIBRARY_PATH') or '').replace(';', ':').split(':')\
             + (os.getenv('PATH') or '').replace(';', ':').split(':')
        self.encoding = 'utf-8'
        if sys.platform == 'win32':
            self.auto_postfix = ''
            self.auto_prefix = ''
            self.load_library = ctypes.windll.LoadLibrary
        else:
            self.auto_postfix = '.so'
            self.auto_prefix = 'lib'
            self.load_library = ctypes.CDLL
        self.config_path = os.path.join(self.cwd, 'config.json')
        if not os.path.isfile(self.config_path):
            self.write_json(
                os.path.join(self.cwd, 'config.json'), self.read_json(os.path.join(self.cwd, 'default_config.json'))
            )
        self.config = self.read_json(self.config_path)
        try:
            if '--client-only' in self.argv:
                raise RuntimeError('Client Only!')
            if self.config['com_type'] == 'tcp':
                self.server: com_base.BaseServer = com_socket.SocketServer(self)
            else:
                raise FileNotFoundError('Unknown communication type')
        except RuntimeError:
            if self.config['com_type'] == 'tcp':
                self.client: com_base.BaseClient = com_socket.SocketClient(self)
            else:
                raise FileNotFoundError('Unknown communication type')
            if self.argv:
                self.client.send(';'.join(self.argv))
                self.exit_code = 0
                # self.client.send('disconnect')
            else:
                self.client_prompt()
            self.client.destroy()
            # self.exit_code = 0
            return
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
            raise FileNotFoundError('Unknown audio backend')
        self.bk.init()
        self.volume = self.config['volume']
        self.speed = self.config['speed']
        if self.volume > 1.0:
            raise RuntimeError(f'Volume {self.volume} is bigger than 1.0')
        self.full_list = []
        for arg in self.argv:
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
            self.server.update()
            self.poll_commands()
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
            log.info(f'{os.path.splitext(mus.fn)[0]}')
            self.play_new_music(mus)
            self.track_loop()

    def play_new_music(self, mus: backend_base.BaseMusic) -> None:
        if self.current_music:
            self.current_music.stop()
            self.current_music.destroy()
        mus.play()
        mus.set_volume(self.volume)
        mus.set_speed(self.speed)
        self.current_music = mus

    def poll_commands(self) -> None:
        temp_mus = []
        while self.server.commands:
            cmds = self.server.commands.pop(0)
            for _cmd in cmds.split(';'):
                cmd = _cmd.strip()
                if os.path.isfile(cmd):
                    temp_mus.append(cmd)
                    continue
                if cmd == 'next':
                    if self.current_music:
                        self.current_music.stop()
                elif cmd == 'toggle_pause':
                    if self.current_music:
                        self.current_music.paused = not self.current_music.paused
                        self.current_music.set_paused(self.current_music.paused)
                        log.info('Paused:', self.current_music.paused)
                elif cmd == '--client-only':
                    pass
                elif cmd.startswith('volume'):
                    try:
                        new_volume = float(cmd.split(' ')[-1])
                    except (ValueError, IndexError) as _err:
                        log.warn(f'Could not convert volume value:', _err)
                        continue
                    if cmd.startswith('volume '):
                        self.volume = 0.0
                    self.volume = max(min(self.volume + new_volume, 1.0), 0.0)
                    if self.current_music:
                        self.current_music.set_volume(self.volume)
                    log.info('New Volume: ', self.volume)
                elif cmd.startswith('speed'):
                    try:
                        new_speed = float(cmd.split(' ')[-1])
                    except (ValueError, IndexError) as _err:
                        log.warn(f'Could not convert speed value:', _err)
                        continue
                    if cmd.startswith('speed '):
                        self.speed = 0.0
                    self.speed = max(min(self.speed + new_speed, 1000.0), 0.0)
                    if self.current_music:
                        self.current_music.set_speed(self.speed)
                    log.info('New Speed: ', self.speed)
                elif cmd == 'exit' or cmd == 'quit':
                    self.running = False
                else:
                    log.warn('Unknown Command', cmd)

    def cleanup(self) -> None:
        if self.server:
            self.server.destroy()
            # self.server = None
        if self.current_music:
            self.current_music.stop()
            self.current_music.destroy()
            self.current_music = None

    def client_prompt(self) -> None:
        msg = 'i_want_to_live_please_do\'nt_die'
        while msg is not None:
            try:
                self.client.send(msg)
                if msg == 'disconnect' or msg == 'exit' or msg == 'quit':
                    self.exit_code = 0
                    return
            except RuntimeError:
                return
            msg = input('>>> ')

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
                    result[lib] = self.load_library(
                        os.path.join(path, prefix + lib) + self.auto_postfix
                    )
                except (FileNotFoundError, OSError):
                    continue
        for lib in libs:
            if result.get(lib):
                continue
            try:
                result[lib] = self.load_library(prefix + lib + self.auto_postfix)
            except (FileNotFoundError, OSError):
                continue
        return result


if __name__ == '__main__':
    sys.exit(App(sys.argv).exit_code)
