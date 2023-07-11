import ctypes
import base_backend
import log


class SDL2Wrapper(base_backend.BaseWrapper):
    def __init__(self, sdl2_lib: ctypes.CDLL, is_le: bool = True) -> None:
        super().__init__()
        self.lib = sdl2_lib
        if not self.lib:
            raise FileNotFoundError('Failed to load SDL2 library')
        self.SDL_AUDIO_F32LSB = 0x8120
        self.SDL_AUDIO_F32MSB = 0x9120
        if is_le:
            self.SDL_AUDIO_F32SYS = self.SDL_AUDIO_F32LSB
        else:
            self.SDL_AUDIO_F32SYS = self.SDL_AUDIO_F32MSB
        self.SDL_AUDIO_ALLOW_FREQUENCY_CHANGE = 0x00000001
        self.SDL_AUDIO_ALLOW_FORMAT_CHANGE = 0x00000002
        self.SDL_AUDIO_ALLOW_CHANNELS_CHANGE = 0x00000004
        self.SDL_AUDIO_ALLOW_SAMPLES_CHANGE = 0x00000008
        self.SDL_AUDIO_ALLOW_ANY_CHANGE = (
            self.SDL_AUDIO_ALLOW_FREQUENCY_CHANGE | self.SDL_AUDIO_ALLOW_FORMAT_CHANGE |
            self.SDL_AUDIO_ALLOW_CHANNELS_CHANGE | self.SDL_AUDIO_ALLOW_SAMPLES_CHANGE
        )
        ver_buf = ctypes.c_buffer(3)  # Lol why we need struct?
        self.SDL_GetVersion = self.wrap('SDL_GetVersion', args=(ctypes.c_void_p, ))
        self.SDL_GetVersion(ver_buf)
        self.ver = (int.from_bytes(ver_buf[0], 'little'), int.from_bytes(ver_buf[1], 'little'),
                    int.from_bytes(ver_buf[2], 'little'))
        self.SDL_AudioInit = self.wrap('SDL_AudioInit', args=(ctypes.c_char_p, ), res=ctypes.c_int)
        self.SDL_AudioQuit = self.wrap('SDL_AudioQuit')
        self.SDL_GetError = self.wrap('SDL_GetError', res=ctypes.c_char_p)
        self.SDL_GetRevision = self.wrap('SDL_GetRevision', res=ctypes.c_char_p)


class SDL2MixWrapper(base_backend.BaseWrapper):
    def __init__(self, sdl2_mixer_lib: ctypes.CDLL) -> None:
        super().__init__()
        self.lib = sdl2_mixer_lib
        if not self.lib:
            raise FileNotFoundError('Failed to load SDL2_mixer library')
        self.Mix_Linked_Version = self.wrap('Mix_Linked_Version', res=ctypes.POINTER(ctypes.c_uint8 * 3))
        self.ver = tuple(self.Mix_Linked_Version().contents[0:3])
        self.Mix_Init = self.wrap('Mix_Init', args=(ctypes.c_int, ), res=ctypes.c_int)
        self.Mix_Quit = self.wrap('Mix_Quit')
        self.Mix_OpenAudioDevice = self.wrap('Mix_OpenAudioDevice', args=(
            ctypes.c_int, ctypes.c_uint16, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int
        ), res=ctypes.c_int)
        self.Mix_CloseAudio = self.wrap('Mix_CloseAudio')


class SDL2Backend(base_backend.BaseBackend):
    def __init__(self, app: any, libs: dict) -> None:
        super().__init__()
        self.app = app
        self.sdl = SDL2Wrapper(libs.get('SDL2'), app.is_le)
        self.mix = SDL2MixWrapper(libs.get('SDL2_mixer'))

    def init(self) -> None:
        if self.sdl.SDL_AudioInit(self.app.stb(self.app.config['audio_driver']) or None) < 0:
            raise RuntimeError(f'Failed to init SDL2 audio ({self.app.bts(self.sdl.SDL_GetError())})')
        mix_flags = 0
        mix_init_flags = self.mix.Mix_Init(mix_flags)
        if not self.mix.Mix_Init(mix_flags) and mix_flags:
            raise RuntimeError(f'Failed to init SDL2_mixer ({self.app.bts(self.sdl.SDL_GetError())})')
        elif not mix_flags == mix_init_flags:
            log.warn(f'Failed to init some SDL2_mixer formats ({self.app.bts(self.sdl.SDL_GetError())})')
        if self.mix.Mix_OpenAudioDevice(
            self.app.config['freq'],
            self.sdl.SDL_AUDIO_F32SYS,
            self.app.config['channels'],
            self.app.config['chunk_size'],
            self.app.stb(self.app.config['device_name']) or None,
            self.sdl.SDL_AUDIO_ALLOW_ANY_CHANGE
        ) < 0:
            raise RuntimeError(f'Failed to open audio device ({self.app.bts(self.sdl.SDL_GetError())})')

    def quit(self) -> None:
        self.mix.Mix_CloseAudio()
        self.mix.Mix_Quit()
        self.sdl.SDL_AudioQuit()

    def destroy(self) -> None:
        self.app = None
