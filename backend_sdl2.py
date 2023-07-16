import ctypes
import sys

import backend_base
import log


class SDL2Wrapper(backend_base.BaseWrapper):
    def __init__(self, sdl2_lib: ctypes.CDLL, is_le: bool = True) -> None:
        super().__init__()
        self.lib = sdl2_lib
        if not self.lib:
            raise FileNotFoundError('Failed to load SDL2 library')
        self.SDL_MIX_MAX_VOLUME = 128
        self.SDL_AUDIO_S16LSB = 0x8010
        self.SDL_AUDIO_S16MSB = 0x9010
        self.SDL_AUDIO_F32LSB = 0x8120
        self.SDL_AUDIO_F32MSB = 0x9120
        if is_le:
            self.SDL_AUDIO_F32SYS = self.SDL_AUDIO_F32LSB
            self.SDL_AUDIO_S16SYS = self.SDL_AUDIO_S16LSB
        else:
            self.SDL_AUDIO_F32SYS = self.SDL_AUDIO_F32MSB
            self.SDL_AUDIO_S16SYS = self.SDL_AUDIO_S16MSB
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
        if self.ver[1] > 0 or self.ver[2] >= 18:
            self.SDL_GetTicks = self.wrap('SDL_GetTicks64', res=ctypes.c_uint64)
        else:
            self.SDL_GetTicks = self.wrap('SDL_GetTicks', res=ctypes.c_uint64)
        self.SDL_GetNumAudioDrivers = self.wrap('SDL_GetNumAudioDrivers', res=ctypes.c_int)
        self.SDL_GetAudioDriver = self.wrap('SDL_GetAudioDriver', args=(ctypes.c_int, ), res=ctypes.c_char_p)
        self.SDL_GetCurrentAudioDriver = self.wrap('SDL_GetCurrentAudioDriver', res=ctypes.c_char_p)
        if self.ver[1] > 0 or self.ver[2] >= 16:
            self.SDL_GetDefaultAudioInfo = self.wrap('SDL_GetDefaultAudioInfo', args=(
                ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int
            ), res=ctypes.c_int)
        else:
            self.SDL_GetDefaultAudioInfo = None


class SDL2MixWrapper(backend_base.BaseWrapper):
    def __init__(self, sdl2_mixer_lib: ctypes.CDLL) -> None:
        super().__init__()
        self.lib = sdl2_mixer_lib
        if not self.lib:
            raise FileNotFoundError('Failed to load SDL2_mixer library')
        self.MIX_INIT_FLAC = 0x00000001
        self.MIX_INIT_MOD = 0x00000002
        self.MIX_INIT_MP3 = 0x00000008
        self.MIX_INIT_OGG = 0x00000010
        self.MIX_INIT_MID = 0x00000020
        self.MIX_INIT_OPUS = 0x00000040
        self.MIX_INIT_WAV_PACK = 0x00000080
        self.MIX_DEFAULT_FREQUENCY = 44100
        self.MIX_DEFAULT_CHANNELS = 2
        self.MIX_NO_FADING = 0
        self.MIX_FADING_OUT = 1
        self.MIX_FADING_IN = 2
        self.MUS_NONE = 0
        self.MUS_CMD = 1
        self.MUS_WAV = 2
        self.MUS_MOD = 3
        self.MUS_MID = 4
        self.MUS_OGG = 5
        self.MUS_MP3 = 6
        self.MUS_MP3_MAD_UNUSED = 7
        self.MUS_FLAC = 8
        self.MUS_MOD_PLUG_UNUSED = 9
        self.MUS_OPUS = 10
        self.MUS_WAV_PACK = 11
        self.MUS_GME = 12
        self.type_map = {
            self.MUS_NONE: 'none',
            self.MUS_CMD: 'cmd',
            self.MUS_WAV: 'wav',
            self.MUS_MOD: 'mod',
            self.MUS_MID: 'mid',
            self.MUS_OGG: 'ogg',
            self.MUS_MP3: 'mp3',
            self.MUS_MP3_MAD_UNUSED: 'mp3',
            self.MUS_FLAC: 'flac',
            self.MUS_MOD_PLUG_UNUSED: 'mod',
            self.MUS_OPUS: 'opus',
            self.MUS_WAV_PACK: 'wav_pack',
            self.MUS_GME: 'gme'
        }
        self.Mix_Linked_Version = self.wrap('Mix_Linked_Version', res=ctypes.POINTER(ctypes.c_uint8 * 3))
        self.ver = tuple(self.Mix_Linked_Version().contents[0:3])
        self.Mix_Init = self.wrap('Mix_Init', args=(ctypes.c_int, ), res=ctypes.c_int)
        self.Mix_Quit = self.wrap('Mix_Quit')
        if self.ver[1] > 0 or self.ver[2] >= 2:
            self.Mix_OpenAudio = None
            self.Mix_OpenAudioDevice = self.wrap('Mix_OpenAudioDevice', args=(
                ctypes.c_int, ctypes.c_uint16, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int
            ), res=ctypes.c_int)
        else:
            self.Mix_OpenAudio = self.wrap('Mix_OpenAudio', args=(
                ctypes.c_int, ctypes.c_uint16, ctypes.c_int, ctypes.c_int
            ), res=ctypes.c_int)
            self.Mix_OpenAudioDevice = None
        self.Mix_CloseAudio = self.wrap('Mix_CloseAudio')
        self.Mix_QuerySpec = self.wrap('Mix_QuerySpec', args=(
            ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(ctypes.c_int)
        ))
        self.Mix_AllocateChannels = self.wrap('Mix_AllocateChannels', args=(ctypes.c_int, ), res=ctypes.c_int)
        self.Mix_LoadMUS = self.wrap('Mix_LoadMUS', args=(ctypes.c_char_p, ), res=ctypes.c_void_p)
        self.Mix_FreeMusic = self.wrap('Mix_FreeMusic', args=(ctypes.c_void_p, ))
        self.Mix_GetMusicType = self.wrap('Mix_GetMusicType', args=(ctypes.c_void_p, ), res=ctypes.c_int)
        self.Mix_PlayMusic = self.wrap('Mix_PlayMusic', args=(ctypes.c_void_p, ctypes.c_int), res=ctypes.c_int)
        self.Mix_FadeInMusic = self.wrap('Mix_FadeInMusic', args=(
            ctypes.c_void_p, ctypes.c_int, ctypes.c_int
        ), res=ctypes.c_int)
        self.Mix_FadeInMusicPos = self.wrap('Mix_FadeInMusicPos', args=(
            ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_double
        ), res=ctypes.c_int)
        self.Mix_FadeOutMusic = self.wrap('Mix_FadeOutMusic', args=(ctypes.c_int, ), res=ctypes.c_int)
        self.Mix_SetMusicPosition = self.wrap('Mix_SetMusicPosition', args=(ctypes.c_double, ), res=ctypes.c_int)
        if self.ver[1] >= 6:
            self.Mix_GetMusicPosition = self.wrap('Mix_GetMusicPosition', args=(ctypes.c_void_p, ), res=ctypes.c_double)
            self.Mix_MusicDuration = self.wrap('Mix_MusicDuration', args=(ctypes.c_void_p, ), res=ctypes.c_double)
        else:
            self.Mix_GetMusicPosition = None
            self.Mix_MusicDuration = None
        self.Mix_PlayingMusic = self.wrap('Mix_PlayingMusic', res=ctypes.c_int)
        self.Mix_PausedMusic = self.wrap('Mix_PausedMusic', res=ctypes.c_int)
        self.Mix_FadingMusic = self.wrap('Mix_FadingMusic', res=ctypes.c_int)
        self.Mix_HaltMusic = self.wrap('Mix_HaltMusic', res=ctypes.c_int)
        self.Mix_VolumeMusic = self.wrap('Mix_VolumeMusic', args=(ctypes.c_void_p, ), res=ctypes.c_int)
        self.Mix_PauseMusic = self.wrap('Mix_PauseMusic')
        self.Mix_ResumeMusic = self.wrap('Mix_ResumeMusic')
        self.Mix_RewindMusic = self.wrap('Mix_RewindMusic')


class SDL2Music(backend_base.BaseMusic):
    def __init__(self, app: any, sdl: SDL2Wrapper, mix: SDL2MixWrapper, fp: str, mus: ctypes.c_void_p) -> None:
        super().__init__(fp)
        self.app = app
        self.sdl = sdl
        self.mix = mix
        self.mus = mus
        self.type = self.mix.type_map.get(self.mix.Mix_GetMusicType(self.mus)) or 'none'
        if self.mix.Mix_MusicDuration:
            self.length = self.mix.Mix_MusicDuration(self.mus)
            if self.length <= 0:
                self.length = 0.0
                log.warn(f'Failed to get music length ({self.app.bts(self.sdl.SDL_GetError())})')

    def play(self) -> None:
        result = self.mix.Mix_PlayMusic(self.mus, 0)
        if result < 0:
            log.warn(f'Failed to play music ({self.app.bts(self.sdl.SDL_GetError())})')

    def set_pos(self, pos: float) -> None:
        if self.mix.Mix_SetMusicPosition(pos) < 0:
            log.warn(f'Failed to set music position ({self.app.bts(self.sdl.SDL_GetError())})')

    def get_pos(self) -> float:
        if not self.mix.Mix_GetMusicPosition:
            return 0.0
        pos = self.mix.Mix_GetMusicPosition(self.mus)
        if pos <= 0:
            pos = 0.0
            log.warn(f'Failed to get music position ({self.app.bts(self.sdl.SDL_GetError())})')
        return pos

    def stop(self) -> None:
        self.mix.Mix_HaltMusic()

    def is_playing(self) -> bool:
        return self.mix.Mix_PlayingMusic()

    def set_paused(self, paused: bool) -> None:
        (self.mix.Mix_PauseMusic if paused else self.mix.Mix_ResumeMusic)()

    def rewind(self) -> None:
        if not self.is_playing():
            return
        self.mix.Mix_RewindMusic()

    def set_volume(self, volume: float = 1.0) -> None:
        self.mix.Mix_VolumeMusic(int(volume * self.sdl.SDL_MIX_MAX_VOLUME))

    def destroy(self) -> None:
        if not self.mix:
            return
        if self.mus:
            self.mix.Mix_FreeMusic(self.mus)
            self.mus = None
        self.mix = None
        self.sdl = None
        self.app = None


class SDL2Backend(backend_base.BaseBackend):
    def __init__(self, app: any, libs: dict) -> None:
        super().__init__()
        self.app = app
        self.sdl = SDL2Wrapper(libs.get('SDL2'), app.is_le)
        self.mix = SDL2MixWrapper(libs.get('SDL2_mixer'))

    def init(self) -> None:
        if self.sdl.SDL_AudioInit(self.app.stb(self.app.config['audio_driver']) or None) < 0:
            raise RuntimeError(f'Failed to init SDL2 audio ({self.app.bts(self.sdl.SDL_GetError())})')
        mix_flags = 0
        if 'mp3' in self.app.config['formats']:
            mix_flags |= self.mix.MIX_INIT_MP3
        if 'ogg' in self.app.config['formats']:
            mix_flags |= self.mix.MIX_INIT_OGG
        if 'opus' in self.app.config['formats']:
            mix_flags |= self.mix.MIX_INIT_OPUS
        if 'mid' in self.app.config['formats']:
            mix_flags |= self.mix.MIX_INIT_MID
        if 'mod' in self.app.config['formats']:
            mix_flags |= self.mix.MIX_INIT_MOD
        if 'flac' in self.app.config['formats']:
            mix_flags |= self.mix.MIX_INIT_FLAC
        mix_init_flags = self.mix.Mix_Init(mix_flags)
        if not self.mix.Mix_Init(mix_flags) and mix_flags:
            raise RuntimeError(f'Failed to init SDL2_mixer ({self.app.bts(self.sdl.SDL_GetError())})')
        elif not mix_flags == mix_init_flags:
            log.warn(f'Failed to init some SDL2_mixer formats ({self.app.bts(self.sdl.SDL_GetError())})')
        if not self.app.config['freq'] or not self.app.config['channels']:
            spec_buf = ctypes.c_buffer(32)
            if not self.sdl.SDL_GetDefaultAudioInfo or self.sdl.SDL_GetDefaultAudioInfo(None, spec_buf, 0):
                log.warn(f'Failed to get default device info ({self.app.bts(self.sdl.SDL_GetError())})')
            else:
                if not self.app.config['freq']:
                    self.app.config['freq'] = int.from_bytes(spec_buf[:4], sys.byteorder, signed=True)  # noqa
                    log.warn('Please set frequency in config to', self.app.config['freq'])
                if not self.app.config['channels']:
                    self.app.config['channels'] = int.from_bytes(spec_buf[6], 'little', signed=True)  # noqa
                    log.warn('Please set channels in config to', self.app.config['channels'])
        if self.mix.Mix_OpenAudioDevice:
            result = self.mix.Mix_OpenAudioDevice(
                self.app.config['freq'],
                self.sdl.SDL_AUDIO_F32SYS if self.app.config['use_float32'] else self.sdl.SDL_AUDIO_S16SYS,
                self.app.config['channels'],
                self.app.config['chunk_size'],
                self.app.stb(self.app.config['device_name']) or None,
                self.sdl.SDL_AUDIO_ALLOW_ANY_CHANGE
            )
        else:
            result = self.mix.Mix_OpenAudio(
                self.app.config['freq'],
                self.sdl.SDL_AUDIO_F32SYS if self.app.config['use_float32'] else self.sdl.SDL_AUDIO_S16SYS,
                self.app.config['channels'],
                self.app.config['chunk_size']
            )
        if result < 0:
            raise RuntimeError(f'Failed to open audio device ({self.app.bts(self.sdl.SDL_GetError())})')
        self.mix.Mix_AllocateChannels(0)

    def open_music(self, fp: str) -> SDL2Music:
        mus = self.mix.Mix_LoadMUS(self.app.stb(fp))
        if not mus:
            raise RuntimeError(f'Failed to open music ({self.app.bts(self.sdl.SDL_GetError())})')
        return SDL2Music(self.app, self.sdl, self.mix, fp, mus)

    def quit(self) -> None:
        self.mix.Mix_CloseAudio()
        self.mix.Mix_Quit()
        self.sdl.SDL_AudioQuit()

    def destroy(self) -> None:
        self.mix = None
        self.sdl = None
        self.app = None

    def get_audio_drivers(self) -> list:
        result = []
        for i in range(self.sdl.SDL_GetNumAudioDrivers()):
            result.append(self.app.bts(self.sdl.SDL_GetAudioDriver(i)))
        return result

    def get_current_audio_driver(self) -> str:
        char_name = self.sdl.SDL_GetCurrentAudioDriver()
        if char_name:
            return self.app.bts(char_name)
        return ''
