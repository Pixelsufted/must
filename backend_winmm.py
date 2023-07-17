import os
import ctypes
import backend_base
import log


class WinMMWrapper(backend_base.BaseWrapper):
    def __init__(self, mm_lib: ctypes.CDLL) -> None:
        super().__init__()
        self.lib = mm_lib
        if not self.lib:
            raise FileNotFoundError('Failed to load Windows MultiMedia library')
        self.mciSendStringW = self.wrap('mciSendStringW', args=(
            ctypes.c_wchar_p, ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p
        ), res=ctypes.c_ulong)
        self.mciGetErrorStringW = self.wrap('mciGetErrorStringW', args=(
            ctypes.c_ulong, ctypes.c_void_p, ctypes.c_uint
        ), res=ctypes.c_int)


class WinMMMusic(backend_base.BaseMusic):
    def __init__(self, bk: any, fp: str, alias: str) -> None:
        super().__init__(fp)
        self.bk = bk
        self.al = alias
        self.type = os.path.splitext(fp)[-1][1:]
        try:
            self.length = float(bk.send_warn(f'status {self.al} length', 'Failed to get music length')) / 1000
        except:
            self.length = 0.0

    def play(self) -> None:
        self.bk.send_warn(f'play {self.al}', 'Failed to play music')

    def stop(self) -> None:
        self.bk.send_warn(f'stop {self.al}', 'Failed to stop music')

    def is_playing(self) -> bool:
        return self.bk.send_warn(f'status {self.al} mode', 'Failed to get music state') in ('playing', 'paused')

    def set_volume(self, volume: float = 1.0) -> None:
        self.bk.send_warn(f'setaudio {self.al} volume to {round(volume * 1000)}', 'Failed to set music volume')

    def set_speed(self, volume: float = 1.0) -> None:
        self.bk.send_warn(f'set {self.al} speed {round(volume * 1000)}', 'Failed to set music speed')

    def set_paused(self, paused: bool) -> None:
        if paused == self.paused:
            return
        self.paused = paused
        self.bk.send_warn(('pause ' if paused else 'resume ') + self.al, 'Failed to set music paused')

    def set_pos(self, pos: float) -> None:
        self.bk.send_warn(f'seek {self.al} to {round(pos * 1000)}', 'Failed to set music position')

    def get_pos(self) -> float:
        res = self.bk.send_warn(f'status {self.al} position', 'Failed to get music position')
        try:
            return float(res) / 1000
        except ValueError:
            return 0.0

    def rewind(self) -> None:
        self.set_pos(0.0)

    def destroy(self) -> None:
        self.bk.send_warn(f'close {self.al}', 'Failed to close music')
        self.bk = None


class WinMMBackend(backend_base.BaseBackend):
    def __init__(self, app: any, mm_lib: ctypes.CDLL) -> None:
        super().__init__()
        self.title = 'WindowsMultimedia'
        self.app = app
        self.buffer_size = 1024
        self.mm = WinMMWrapper(mm_lib)

    def open_music(self, fp: str) -> WinMMMusic:
        alias = os.path.basename(fp).replace(' ', '')
        self.send_err(f'open "{fp}" alias {alias}', 'Failed to open music')
        self.send_warn(f'set {alias} time format milliseconds', 'Failed to set time format for music')
        return WinMMMusic(self, fp, alias)

    def destroy(self) -> None:
        self.mm = None
        self.app = None

    def get_audio_devices_names(self) -> list:
        return ['Default Device']

    def get_audio_drivers(self) -> list:
        return ['winmm']

    def get_current_audio_driver(self) -> str:
        return 'winmm'

    def get_current_audio_device_name(self) -> str:
        return 'Default Device'

    def send(self, command: str) -> tuple:
        buffer = ctypes.create_unicode_buffer(self.buffer_size + 1)
        code = self.mm.mciSendStringW(command, buffer, self.buffer_size, None)
        if code:
            new_buf = ctypes.create_unicode_buffer(self.buffer_size + 1)
            if self.mm.mciGetErrorStringW(code, buffer, self.buffer_size):
                return new_buf.value, True
            return 'Unknown Error', True
        return buffer.value, False

    def send_err(self, command: str, error_text: str) -> str:
        resp, is_err = self.send(command)
        if is_err:
            raise RuntimeError(error_text + ' (' + resp + ')')
        return resp

    def send_warn(self, command: str, error_text: str) -> str:
        resp, is_err = self.send(command)
        if is_err:
            log.warn(error_text + ' (' + resp + ')')
            return ''
        return resp
