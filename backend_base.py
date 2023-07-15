import os
import ctypes
import log


class BaseWrapper:
    def __init__(self) -> None:
        self.lib: ctypes.CDLL = None  # noqa

    def wrap(self, func_name: str, args: tuple = (), res: any = ctypes.c_void_p) -> any:
        try:
            result = getattr(self.lib, func_name)
        except AttributeError:
            log.warn('Failed to import function', func_name)
            return None
        result.argtypes = args
        result.restype = res
        return result


class BaseMusic:
    def __init__(self, fp: str) -> None:
        self.fp = fp
        self.fn = os.path.basename(fp)
        self.type = 'none'
        self.paused = False
        self.freq = 0.0

    def play(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def set_paused(self, paused: bool) -> None:
        pass

    def is_playing(self) -> bool:
        pass

    def set_volume(self, volume: float = 1.0) -> None:
        pass

    def set_speed(self, speed: float = 1.0) -> None:
        pass

    def destroy(self) -> None:
        pass


class BaseBackend:
    def __init__(self) -> None:
        pass

    def init(self) -> None:
        pass

    def open_music(self, fp: str) -> BaseMusic:
        pass

    def quit(self) -> None:
        pass

    def destroy(self) -> None:
        pass

    def get_audio_drivers(self) -> list:
        pass

    def get_current_audio_driver(self) -> str:
        pass

    def update(self) -> None:
        pass
