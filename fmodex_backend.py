import ctypes
import base_backend
import log


class FmodExWrapper(base_backend.BaseWrapper):
    def __init__(self, fmod_lib: ctypes.CDLL, is_le: bool = True) -> None:
        super().__init__()
        self.lib = fmod_lib
        if not self.lib:
            raise FileNotFoundError('Failed to load FmodEx library')


class FmodExMusic(base_backend.BaseMusic):
    def __init__(self, app: any, fmod: FmodExWrapper, fp: str, mus: ctypes.c_void_p) -> None:
        super().__init__(fp)
        self.app = app
        self.fmod = fmod
        self.mus = mus

    def play(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def is_playing(self) -> None:
        pass

    def set_paused(self, paused: bool) -> None:
        pass

    def rewind(self) -> None:
        pass

    def set_volume(self, volume: float = 1.0) -> None:
        pass

    def destroy(self) -> None:
        if not self.fmod:
            return
        self.fmod = None
        self.app = None


class FmodExBackend(base_backend.BaseBackend):
    def __init__(self, app: any, libs: dict) -> None:
        super().__init__()
        self.app = app
        self.fmod = FmodExWrapper(libs.get('fmod'), app.is_le)

    def init(self) -> None:
        pass

    def open_music(self, fp: str) -> FmodExMusic:
        pass

    def quit(self) -> None:
        pass

    def destroy(self) -> None:
        self.app = None

    def get_audio_drivers(self) -> list:
        pass

    def get_current_audio_driver(self) -> str:
        pass
