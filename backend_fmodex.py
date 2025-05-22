import sys
import ctypes
import backend_base
import log


class FmodExWrapper(backend_base.BaseWrapper):
    def __init__(self, fmod_lib: ctypes.CDLL) -> None:
        super().__init__()
        self.lib = fmod_lib
        if not self.lib:
            raise FileNotFoundError('Failed to load FmodEx library')
        # TODO: prettify
        # - Errors -
        self.FMOD_OK = 0
        self.FMOD_ERR_BAD_COMMAND = 1
        self.FMOD_ERR_CHANNEL_ALLOC = 2
        self.FMOD_ERR_CHANNEL_STOLEN = 3
        self.FMOD_ERR_DMA = 4
        self.FMOD_ERR_DSP_CONNECTION = 5
        self.FMOD_ERR_DSP_DONT_PROCESS = 6
        self.FMOD_ERR_DSP_FORMAT = 7
        self.FMOD_ERR_DSP_INUSE = 8
        self.FMOD_ERR_DSP_NOTFOUND = 9
        self.FMOD_ERR_DSP_RESERVED = 10
        self.FMOD_ERR_DSP_SILENCE = 11
        self.FMOD_ERR_DSP_TYPE = 12
        self.FMOD_ERR_FILE_BAD = 13
        self.FMOD_ERR_FILE_COULD_NOT_SEEK = 14
        self.FMOD_ERR_FILE_DISK_EJECTED = 15
        self.FMOD_ERR_FILE_EOF = 16
        self.FMOD_ERR_FILE_END_OF_DATA = 17
        self.FMOD_ERR_FILE_NOTFOUND = 18
        self.FMOD_ERR_FORMAT = 19
        self.FMOD_ERR_HEADER_MISMATCH = 20
        self.FMOD_ERR_HTTP = 21
        self.FMOD_ERR_HTTP_ACCESS = 22
        self.FMOD_ERR_HTTP_PROXY_AUTH = 23
        self.FMOD_ERR_HTTP_SERVER_ERROR = 24
        self.FMOD_ERR_HTTP_TIMEOUT = 25
        self.FMOD_ERR_INITIALIZATION = 26
        self.FMOD_ERR_INITIALIZED = 27
        self.FMOD_ERR_INTERNAL = 28
        self.FMOD_ERR_INVALID_FLOAT = 29
        self.FMOD_ERR_INVALID_HANDLE = 30
        self.FMOD_ERR_INVALID_PARAM = 31
        self.FMOD_ERR_INVALID_POSITION = 32
        self.FMOD_ERR_INVALID_SPEAKER = 33
        self.FMOD_ERR_INVALID_SYNC_POINT = 34
        self.FMOD_ERR_INVALID_THREAD = 35
        self.FMOD_ERR_INVALID_VECTOR = 36
        self.FMOD_ERR_MAX_AUDIBLE = 37
        self.FMOD_ERR_MEMORY = 38
        self.FMOD_ERR_MEMORY_CANT_POINT = 39
        self.FMOD_ERR_NEEDS3D = 40
        self.FMOD_ERR_NEED_SHARD_WARE = 41
        self.FMOD_ERR_NET_CONNECT = 42
        self.FMOD_ERR_NET_SOCKET_ERROR = 43
        self.FMOD_ERR_NET_URL = 44
        self.FMOD_ERR_NET_WOULD_BLOCK = 45
        self.FMOD_ERR_NOT_READY = 46
        self.FMOD_ERR_OUTPUT_ALLOCATED = 47
        self.FMOD_ERR_OUTPUT_CREATE_BUFFER = 48
        self.FMOD_ERR_OUTPUT_DRIVER_CALL = 49
        self.FMOD_ERR_OUTPUT_FORMAT = 50
        self.FMOD_ERR_OUTPUT_INIT = 51
        self.FMOD_ERR_OUTPUT_NO_DRIVERS = 52
        self.FMOD_ERR_PLUGIN = 53
        self.FMOD_ERR_PLUGIN_MISSING = 54
        self.FMOD_ERR_PLUGIN_RESOURCE = 55
        self.FMOD_ERR_PLUGIN_VERSION = 56
        self.FMOD_ERR_RECORD = 57
        self.FMOD_ERR_REVERB_CHANNEL_GROUP = 58
        self.FMOD_ERR_REVERB_INSTANCE = 59
        self.FMOD_ERR_SUB_SOUNDS = 60
        self.FMOD_ERR_SUB_SOUND_ALLOCATED = 61
        self.FMOD_ERR_SUB_SOUND_CANT_MOVE = 62
        self.FMOD_ERR_TAG_NOT_FOUND = 63
        self.FMOD_ERR_TOO_MANY_CHANNELS = 64
        self.FMOD_ERR_TRUNCATED = 65
        self.FMOD_ERR_UNIMPLEMENTED = 66
        self.FMOD_ERR_UNINITIALIZED = 67
        self.FMOD_ERR_UNSUPPORTED = 68
        self.FMOD_ERR_VERSION = 69
        self.FMOD_ERR_EVENT_ALREADY_LOADED = 70
        self.FMOD_ERR_EVENT_LIVE_UPDATE_BUSY = 71
        self.FMOD_ERR_EVENT_LIVE_UPDATE_MISMATCH = 72
        self.FMOD_ERR_EVENT_LIVE_UPDATE_TIMEOUT = 73
        self.FMOD_ERR_EVENT_NOTFOUND = 74
        self.FMOD_ERR_STUDIO_UNINITIALIZED = 75
        self.FMOD_ERR_STUDIO_NOT_LOADED = 76
        self.FMOD_ERR_INVALID_STRING = 77
        self.FMOD_ERR_ALREADY_LOCKED = 78
        self.FMOD_ERR_NOT_LOCKED = 79
        self.FMOD_ERR_RECORD_DISCONNECTED = 80
        self.FMOD_ERR_TOO_MANY_SAMPLES = 81
        self.error_map = {
            self.FMOD_OK: "No errors.",
            self.FMOD_ERR_BAD_COMMAND: "Tried to call a function on a data type that does not allow this type of"
                                       " functionality (ie calling Sound::lock on a streaming sound).",
            self.FMOD_ERR_CHANNEL_ALLOC: "Error trying to allocate a channel.",
            self.FMOD_ERR_CHANNEL_STOLEN: "The specified channel has been reused to play another sound.",
            self.FMOD_ERR_DMA: "DMA Failure.  See debug output for more information.",
            self.FMOD_ERR_DSP_CONNECTION: "DSP connection error.  Connection possibly caused a cyclic dependency or"
                                          " connected dsps with incompatible buffer counts.",
            self.FMOD_ERR_DSP_DONT_PROCESS: "DSP return code from a DSP process query callback.  Tells mixer not to"
                                            " call the process callback and therefore not consume CPU.  Use this to"
                                            " optimize the DSP graph.",
            self.FMOD_ERR_DSP_FORMAT: "DSP Format error.  A DSP unit may have attempted to connect to this network"
                                      " with the wrong format, or a matrix may have been set with the wrong size"
                                      " if the target unit has a specified channel map.",
            self.FMOD_ERR_DSP_INUSE: "DSP is already in the mixer's DSP network. It must be removed before being"
                                     " reinserted or released.",
            self.FMOD_ERR_DSP_NOTFOUND: "DSP connection error.  Couldn't find the DSP unit specified.",
            self.FMOD_ERR_DSP_RESERVED: "DSP operation error.  Cannot perform operation on this DSP as it is reserved"
                                        " by the system.",
            self.FMOD_ERR_DSP_SILENCE: "DSP return code from a DSP process query callback.  Tells mixer silence would"
                                       " be produced from read, so go idle and not consume CPU.  Use this to optimize"
                                       " the DSP graph.",
            self.FMOD_ERR_DSP_TYPE: "DSP operation cannot be performed on a DSP of this type.",
            self.FMOD_ERR_FILE_BAD: "Error loading file.",
            self.FMOD_ERR_FILE_COULD_NOT_SEEK: "Couldn't perform seek operation.  This is a limitation of the medium"
                                               " (ie netstreams) or the file format.",
            self.FMOD_ERR_FILE_DISK_EJECTED: "Media was ejected while reading.",
            self.FMOD_ERR_FILE_EOF: "End of file unexpectedly reached while trying to read essential data"
                                    " (truncated?).",
            self.FMOD_ERR_FILE_END_OF_DATA: "End of current chunk reached while trying to read data.",
            self.FMOD_ERR_FILE_NOTFOUND: "File not found.",
            self.FMOD_ERR_FORMAT: "Unsupported file or audio format.",
            self.FMOD_ERR_HEADER_MISMATCH: "There is a version mismatch between the FMOD header and either the FMOD"
                                           " Studio library or the FMOD Low Level library.",
            self.FMOD_ERR_HTTP: "A HTTP error occurred. This is a catch-all for HTTP errors not listed elsewhere.",
            self.FMOD_ERR_HTTP_ACCESS: "The specified resource requires authentication or is forbidden.",
            self.FMOD_ERR_HTTP_PROXY_AUTH: "Proxy authentication is required to access the specified resource.",
            self.FMOD_ERR_HTTP_SERVER_ERROR: "A HTTP server error occurred.",
            self.FMOD_ERR_HTTP_TIMEOUT: "The HTTP request timed out.",
            self.FMOD_ERR_INITIALIZATION: "FMOD was not initialized correctly to support this function.",
            self.FMOD_ERR_INITIALIZED: "Cannot call this command after System::init.",
            self.FMOD_ERR_INTERNAL: "An error occurred that wasn't supposed to.  Contact support.",
            self.FMOD_ERR_INVALID_FLOAT: "Value passed in was a NaN, Inf or denormalized float.",
            self.FMOD_ERR_INVALID_HANDLE: "An invalid object handle was used.",
            self.FMOD_ERR_INVALID_PARAM: "An invalid parameter was passed to this function.",
            self.FMOD_ERR_INVALID_POSITION: "An invalid seek position was passed to this function.",
            self.FMOD_ERR_INVALID_SPEAKER: "An invalid speaker was passed to this function based on the current"
                                           " speaker mode.",
            self.FMOD_ERR_INVALID_SYNC_POINT: "The syncpoint did not come from this sound handle.",
            self.FMOD_ERR_INVALID_THREAD: "Tried to call a function on a thread that is not supported.",
            self.FMOD_ERR_INVALID_VECTOR: "The vectors passed in are not unit length, or perpendicular.",
            self.FMOD_ERR_MAX_AUDIBLE: "Reached maximum audible playback count for this sound's soundgroup.",
            self.FMOD_ERR_MEMORY: "Not enough memory or resources.",
            self.FMOD_ERR_MEMORY_CANT_POINT: "Can't use FMOD_OPENMEMORY_POINT on non PCM source data, or non"
                                             " mp3/xma/adpcm data if FMOD_CREATECOMPRESSEDSAMPLE was used.",
            self.FMOD_ERR_NEEDS3D: "Tried to call a command on a 2d sound when the command was meant for 3d sound.",
            self.FMOD_ERR_NEED_SHARD_WARE: "Tried to use a feature that requires hardware support.",
            self.FMOD_ERR_NET_CONNECT: "Couldn't connect to the specified host.",
            self.FMOD_ERR_NET_SOCKET_ERROR: "A socket error occurred.  This is a catch-all for socket-related errors"
                                            " not listed elsewhere.",
            self.FMOD_ERR_NET_URL: "The specified URL couldn't be resolved.",
            self.FMOD_ERR_NET_WOULD_BLOCK: "Operation on a non-blocking socket could not complete immediately.",
            self.FMOD_ERR_NOT_READY: "Operation could not be performed because specified sound/DSP connection is not"
                                     " ready.",
            self.FMOD_ERR_OUTPUT_ALLOCATED: "Error initializing output device, but more specifically, the output device"
                                            " is already in use and cannot be reused.",
            self.FMOD_ERR_OUTPUT_CREATE_BUFFER: "Error creating hardware sound buffer.",
            self.FMOD_ERR_OUTPUT_DRIVER_CALL: "A call to a standard soundcard driver failed, which could possibly mean"
                                              " a bug in the driver or resources were missing or exhausted.",
            self.FMOD_ERR_OUTPUT_FORMAT: "Soundcard does not support the specified format.",
            self.FMOD_ERR_OUTPUT_INIT: "Error initializing output device.",
            self.FMOD_ERR_OUTPUT_NO_DRIVERS: "The output device has no drivers installed.  If pre-init,"
                                             " FMOD_OUTPUT_NOSOUND is selected as the output mode.  If post-init,"
                                             " the function just fails.",
            self.FMOD_ERR_PLUGIN: "An unspecified error has been returned from a plugin.",
            self.FMOD_ERR_PLUGIN_MISSING: "A requested output, dsp unit type or codec was not available.",
            self.FMOD_ERR_PLUGIN_RESOURCE: "A resource that the plugin requires cannot be allocated or found."
                                           " (ie the DLS file for MIDI playback)",
            self.FMOD_ERR_PLUGIN_VERSION: "A plugin was built with an unsupported SDK version.",
            self.FMOD_ERR_RECORD: "An error occurred trying to initialize the recording device.",
            self.FMOD_ERR_REVERB_CHANNEL_GROUP: "Reverb properties cannot be set on this channel because a parent"
                                                " channelgroup owns the reverb connection.",
            self.FMOD_ERR_REVERB_INSTANCE: "Specified instance in FMOD_REVERB_PROPERTIES couldn't be set. Most likely"
                                           " because it is an invalid instance number or the reverb doesn't exist.",
            self.FMOD_ERR_SUB_SOUNDS: "The error occurred because the sound referenced contains subsounds when it"
                                      " shouldn't have, or it doesn't contain subsounds when it should have."
                                      "  The operation may also not be able to be performed on a parent sound.",
            self.FMOD_ERR_SUB_SOUND_ALLOCATED: "This subsound is already being used by another sound, you cannot have"
                                               " more than one parent to a sound.  Null out the other parent's entry"
                                               " first.",
            self.FMOD_ERR_SUB_SOUND_CANT_MOVE: "Shared subsounds cannot be replaced or moved from their parent stream,"
                                               " such as when the parent stream is an FSB file.",
            self.FMOD_ERR_TAG_NOT_FOUND: "The specified tag could not be found or there are no tags.",
            self.FMOD_ERR_TOO_MANY_CHANNELS: "The sound created exceeds the allowable input channel count.  This can be"
                                             " increased using the 'maxinputchannels' parameter in"
                                             " System::setSoftwareFormat.",
            self.FMOD_ERR_TRUNCATED: "The retrieved string is too long to fit in the supplied buffer and has been"
                                     " truncated.",
            self.FMOD_ERR_UNIMPLEMENTED: "Something in FMOD hasn't been implemented when it should be!"
                                         " contact support!",
            self.FMOD_ERR_UNINITIALIZED: "This command failed because System::init or System::setDriver"
                                         " was not called.",
            self.FMOD_ERR_UNSUPPORTED: "A command issued was not supported by this object.  Possibly a plugin without"
                                       " certain callbacks specified.",
            self.FMOD_ERR_VERSION: "The version number of this file format is not supported.",
            self.FMOD_ERR_EVENT_ALREADY_LOADED: "The specified bank has already been loaded.",
            self.FMOD_ERR_EVENT_LIVE_UPDATE_BUSY: "The live update connection failed due to the game already being"
                                                  " connected.",
            self.FMOD_ERR_EVENT_LIVE_UPDATE_MISMATCH: "The live update connection failed due to the game data being"
                                                      " out of sync with the tool.",
            self.FMOD_ERR_EVENT_LIVE_UPDATE_TIMEOUT: "The live update connection timed out.",
            self.FMOD_ERR_EVENT_NOTFOUND: "The requested event, parameter, bus or vca could not be found.",
            self.FMOD_ERR_STUDIO_UNINITIALIZED: "The Studio::System object is not yet initialized.",
            self.FMOD_ERR_STUDIO_NOT_LOADED: "The specified resource is not loaded, so it can't be unloaded.",
            self.FMOD_ERR_INVALID_STRING: "An invalid string was passed to this function.",
            self.FMOD_ERR_ALREADY_LOCKED: "The specified resource is already locked.",
            self.FMOD_ERR_NOT_LOCKED: "The specified resource is not locked, so it can't be unlocked.",
            self.FMOD_ERR_RECORD_DISCONNECTED: "The specified recording driver has been disconnected.",
            self.FMOD_ERR_TOO_MANY_SAMPLES: "The length provided exceeds the allowable limit.",
        }
        # - Music Formats -
        self.FMOD_SOUND_TYPE_UNKNOWN = 0
        self.FMOD_SOUND_TYPE_AIFF = 1
        self.FMOD_SOUND_TYPE_ASF = 2
        self.FMOD_SOUND_TYPE_DLS = 3
        self.FMOD_SOUND_TYPE_FLAC = 4
        self.FMOD_SOUND_TYPE_FSB = 5
        self.FMOD_SOUND_TYPE_IT = 6
        self.FMOD_SOUND_TYPE_MIDI = 7
        self.FMOD_SOUND_TYPE_MOD = 8
        self.FMOD_SOUND_TYPE_MPEG = 9
        self.FMOD_SOUND_TYPE_OGG_VORBIS = 10
        self.FMOD_SOUND_TYPE_PLAYLIST = 11
        self.FMOD_SOUND_TYPE_RAW = 12
        self.FMOD_SOUND_TYPE_S3M = 13
        self.FMOD_SOUND_TYPE_USER = 14
        self.FMOD_SOUND_TYPE_WAV = 15
        self.FMOD_SOUND_TYPE_XM = 16
        self.FMOD_SOUND_TYPE_XMA = 17
        self.FMOD_SOUND_TYPE_AUDIO_QUEUE = 18
        self.FMOD_SOUND_TYPE_AT9 = 19
        self.FMOD_SOUND_TYPE_VORBIS = 20
        self.FMOD_SOUND_TYPE_MEDIA_FOUNDATION = 21
        self.FMOD_SOUND_TYPE_MEDIA_CODEC = 22
        self.FMOD_SOUND_TYPE_FAD_PCM = 23
        self.FMOD_SOUND_TYPE_OPUS = 24
        self.format_map = {
            self.FMOD_SOUND_TYPE_UNKNOWN: 'none',
            self.FMOD_SOUND_TYPE_AIFF: 'aiff',
            self.FMOD_SOUND_TYPE_ASF: 'asf',
            self.FMOD_SOUND_TYPE_DLS: 'dls',
            self.FMOD_SOUND_TYPE_FLAC: 'flac',
            self.FMOD_SOUND_TYPE_FSB: 'fsb',
            self.FMOD_SOUND_TYPE_IT: 'it',
            self.FMOD_SOUND_TYPE_MIDI: 'mid',
            self.FMOD_SOUND_TYPE_MOD: 'mod',
            self.FMOD_SOUND_TYPE_MPEG: 'mp3',
            self.FMOD_SOUND_TYPE_OGG_VORBIS: 'ogg',
            self.FMOD_SOUND_TYPE_PLAYLIST: 'playlist',
            self.FMOD_SOUND_TYPE_RAW: 'raw',
            self.FMOD_SOUND_TYPE_S3M: 's3m',
            self.FMOD_SOUND_TYPE_USER: 'user',
            self.FMOD_SOUND_TYPE_WAV: 'wav',
            self.FMOD_SOUND_TYPE_XM: 'xm',
            self.FMOD_SOUND_TYPE_XMA: 'xma',
            self.FMOD_SOUND_TYPE_AUDIO_QUEUE: 'audio_queue',
            self.FMOD_SOUND_TYPE_AT9: 'at9',
            self.FMOD_SOUND_TYPE_VORBIS: 'vorbis',
            self.FMOD_SOUND_TYPE_MEDIA_FOUNDATION: 'media_foundation',
            self.FMOD_SOUND_TYPE_MEDIA_CODEC: 'media_codec',
            self.FMOD_SOUND_TYPE_FAD_PCM: 'pcm',
            self.FMOD_SOUND_TYPE_OPUS: 'opus'
        }
        # - Init Flags -
        self.FMOD_INIT_NORMAL = 0x00000000
        self.FMOD_INIT_STREAM_FROM_UPDATE = 0x00000001
        self.FMOD_INIT_MIX_FROM_UPDATE = 0x00000002
        self.FMOD_INIT_3D_RIGHT_HANDED = 0x00000004
        self.FMOD_INIT_CLIP_OUTPUT = 0x00000008
        self.FMOD_INIT_CHANNEL_LOWPASS = 0x00000100
        self.FMOD_INIT_CHANNEL_DISTANCE_FILTER = 0x00000200
        self.FMOD_INIT_PROFILE_ENABLE = 0x00010000
        self.FMOD_INIT_VOL0_BECOMES_VIRTUAL = 0x00020000
        self.FMOD_INIT_GEOMETRY_USE_CLOSEST = 0x00040000
        self.FMOD_INIT_PREFER_DOLBY_DOWN_MIX = 0x00080000
        self.FMOD_INIT_THREAD_UNSAFE = 0x00100000
        self.FMOD_INIT_PROFILE_METER_ALL = 0x00200000
        self.FMOD_INIT_MEMORY_TRACKING = 0x00400000
        # - Music Modes -
        self.FMOD_DEFAULT = 0x00000000
        self.FMOD_LOOP_OFF = 0x00000001
        self.FMOD_LOOP_NORMAL = 0x00000002
        self.FMOD_LOOP_BIDI = 0x00000004
        self.FMOD_2D = 0x00000008
        self.FMOD_3D = 0x00000010
        self.FMOD_CREATE_STREAM = 0x00000080
        self.FMOD_CREATE_SAMPLE = 0x00000100
        self.FMOD_CREATE_COMPRESSED_SAMPLE = 0x00000200
        self.FMOD_OPEN_USER = 0x00000400
        self.FMOD_OPEN_MEMORY = 0x00000800
        self.FMOD_OPEN_MEMORY_POINT = 0x10000000
        self.FMOD_OPEN_RAW = 0x00001000
        self.FMOD_OPEN_ONLY = 0x00002000
        self.FMOD_ACCURATE_TIME = 0x00004000
        self.FMOD_MPEG_SEARCH = 0x00008000
        self.FMOD_NONBLOCKING = 0x00010000
        self.FMOD_UNIQUE = 0x00020000
        self.FMOD_3D_HEAD_RELATIVE = 0x00040000
        self.FMOD_3D_WORLD_RELATIVE = 0x00080000
        self.FMOD_3D_INVERSE_ROLL_OFF = 0x00100000
        self.FMOD_3D_LINEAR_ROLL_OFF = 0x00200000
        self.FMOD_3D_LINEAR_SQUARE_ROLL_OFF = 0x00400000
        self.FMOD_3D_INVERSE_TAPERED_ROLL_OFF = 0x00800000
        self.FMOD_3D_CUSTOM_ROLL_OFF = 0x04000000
        self.FMOD_3D_IGNORE_GEOMETRY = 0x40000000
        self.FMOD_IGNORE_TAGS = 0x02000000
        self.FMOD_LOW_MEM = 0x08000000
        self.FMOD_VIRTUAL_PLAY_FROM_START = 0x80000000
        # - Time Units -
        self.FMOD_TIMEUNIT_MS = 0x00000001
        self.FMOD_TIMEUNIT_PCM = 0x00000002
        self.FMOD_TIMEUNIT_PCM_BYTES = 0x00000004
        self.FMOD_TIMEUNIT_RAW_BYTES = 0x00000008
        self.FMOD_TIMEUNIT_PCM_FRACTION = 0x00000010
        self.FMOD_TIMEUNIT_MOD_ORDER = 0x00000100
        self.FMOD_TIMEUNIT_MOD_ROW = 0x00000200
        self.FMOD_TIMEUNIT_MOD_PATTERN = 0x00000400
        # - Output Types -
        self.FMOD_OUTPUT_TYPE_AUTODETECT = 0
        self.FMOD_OUTPUT_TYPE_UNKNOWN = 1
        self.FMOD_OUTPUT_TYPE_NO_SOUND = 2
        self.FMOD_OUTPUT_TYPE_WAV_WRITER = 3
        self.FMOD_OUTPUT_TYPE_NO_SOUND_NRT = 4
        self.FMOD_OUTPUT_TYPE_WAV_WRITER_NRT = 5
        self.FMOD_OUTPUT_TYPE_WASAPI = 6
        self.FMOD_OUTPUT_TYPE_ASIO = 7
        self.FMOD_OUTPUT_TYPE_PULSEAUDIO = 8
        self.FMOD_OUTPUT_TYPE_ALSA = 9
        self.FMOD_OUTPUT_TYPE_CORE_AUDIO = 10
        self.FMOD_OUTPUT_TYPE_AUDIOTRACK = 11
        self.FMOD_OUTPUT_TYPE_OPENSL = 12
        self.FMOD_OUTPUT_TYPE_AUDIO_OUT = 13
        self.FMOD_OUTPUT_TYPE_AUDIO3D = 14
        self.FMOD_OUTPUT_TYPE_WEB_AUDIO = 15
        self.FMOD_OUTPUT_TYPE_NNAUDIO = 16
        self.FMOD_OUTPUT_TYPE_WIN_SONIC = 17
        self.FMOD_OUTPUT_TYPE_A_AUDIO = 18
        self.FMOD_OUTPUT_TYPE_AUDIO_WORK_LET = 19
        self.FMOD_OUTPUT_TYPE_PHASE = 20
        self.output_map = {
            '': self.FMOD_OUTPUT_TYPE_AUTODETECT,
            'auto': self.FMOD_OUTPUT_TYPE_AUTODETECT,
            'dummy': self.FMOD_OUTPUT_TYPE_NO_SOUND,
            'disk': self.FMOD_OUTPUT_TYPE_WAV_WRITER,
            'wasapi': self.FMOD_OUTPUT_TYPE_WASAPI,
            'asio': self.FMOD_OUTPUT_TYPE_ASIO,
            'pulseaudio': self.FMOD_OUTPUT_TYPE_PULSEAUDIO,
            'alsa': self.FMOD_OUTPUT_TYPE_ALSA,
            'coreaudio': self.FMOD_OUTPUT_TYPE_CORE_AUDIO,
            'opensl': self.FMOD_OUTPUT_TYPE_OPENSL,
            'webaudio': self.FMOD_OUTPUT_TYPE_WEB_AUDIO,
            'winsonic': self.FMOD_OUTPUT_TYPE_WIN_SONIC
        }
        self.FMOD_System_Create = self.wrap('FMOD_System_Create', args=(ctypes.POINTER(ctypes.c_void_p), ctypes.c_uint))
        self.FMOD_System_Release = self.wrap('FMOD_System_Release', args=(ctypes.c_void_p,))
        self.FMOD_System_Init = self.wrap('FMOD_System_Init', args=(
            ctypes.c_void_p, ctypes.c_int, ctypes.c_uint, ctypes.c_void_p
        ))
        self.FMOD_System_GetVersion = self.wrap(
            'FMOD_System_GetVersion', args=(ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint))
        )
        self.FMOD_System_Close = self.wrap('FMOD_System_Close', args=(ctypes.c_void_p,))
        self.FMOD_System_CreateStream = self.wrap('FMOD_System_CreateStream', args=(
            ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint, ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p)
        ))
        self.FMOD_Sound_Release = self.wrap('FMOD_Sound_Release', args=(ctypes.c_void_p,))
        self.FMOD_System_PlaySound = self.wrap('FMOD_System_PlaySound', args=(
            ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_void_p)
        ))
        self.FMOD_System_Update = self.wrap('FMOD_System_Update', args=(ctypes.c_void_p,))
        self.FMOD_Channel_Stop = self.wrap('FMOD_Channel_Stop', args=(ctypes.c_void_p,))
        self.FMOD_Channel_SetPaused = self.wrap('FMOD_Channel_SetPaused', args=(ctypes.c_void_p, ctypes.c_int))
        self.FMOD_Channel_SetVolume = self.wrap('FMOD_Channel_SetVolume', args=(ctypes.c_void_p, ctypes.c_float))
        self.FMOD_Channel_SetPitch = self.wrap('FMOD_Channel_SetPitch', args=(ctypes.c_void_p, ctypes.c_float))
        self.FMOD_Channel_GetPitch = self.wrap(
            'FMOD_Channel_GetPitch', args=(ctypes.c_void_p, ctypes.POINTER(ctypes.c_float))
        )
        self.FMOD_Channel_SetFrequency = self.wrap('FMOD_Channel_SetFrequency', args=(ctypes.c_void_p, ctypes.c_float))
        self.FMOD_Channel_GetFrequency = self.wrap(
            'FMOD_Channel_GetFrequency', args=(ctypes.c_void_p, ctypes.POINTER(ctypes.c_float))
        )
        self.FMOD_Channel_IsPlaying = self.wrap(
            'FMOD_Channel_IsPlaying', args=(ctypes.c_void_p, ctypes.POINTER(ctypes.c_int))
        )
        self.FMOD_Sound_GetDefaults = self.wrap('FMOD_Sound_GetDefaults', args=(
            ctypes.c_void_p, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_int)
        ))
        self.FMOD_Sound_GetLength = self.wrap('FMOD_Sound_GetLength', args=(
            ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint), ctypes.c_uint
        ))
        self.FMOD_Channel_GetPosition = self.wrap('FMOD_Channel_GetPosition', args=(
            ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint), ctypes.c_uint
        ))
        self.FMOD_Channel_SetPosition = self.wrap('FMOD_Channel_SetPosition', args=(
            ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint
        ))
        self.FMOD_System_GetOutput = self.wrap('FMOD_System_GetOutput', args=(
            ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)
        ))
        self.FMOD_System_SetOutput = self.wrap('FMOD_System_SetOutput', args=(ctypes.c_void_p, ctypes.c_int))
        self.FMOD_Sound_GetFormat = self.wrap('FMOD_Sound_GetFormat', args=(
            ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)
        ))
        self.FMOD_System_GetNumDrivers = self.wrap(
            'FMOD_System_GetNumDrivers', args=(ctypes.c_void_p, ctypes.POINTER(ctypes.c_int))
        )
        self.FMOD_System_GetDriverInfo = self.wrap('FMOD_System_GetDriverInfo', args=(
            ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(ctypes.c_int),
            ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)
        ))
        self.FMOD_System_SetDriver = self.wrap('FMOD_System_SetDriver', args=(ctypes.c_void_p, ctypes.c_int))
        self.FMOD_System_GetDriver = self.wrap(
            'FMOD_System_GetDriver', args=(ctypes.c_void_p, ctypes.POINTER(ctypes.c_int))
        )
        self.FMOD_System_SetSoftwareChannels = self.wrap(
            'FMOD_System_SetSoftwareChannels', args=(ctypes.c_void_p, ctypes.c_int)
        )
        self.FMOD_System_GetSoftwareChannels = self.wrap(
            'FMOD_System_GetSoftwareChannels', args=(ctypes.c_void_p, ctypes.POINTER(ctypes.c_int))
        )
        self.FMOD_System_SetSoftwareFormat = self.wrap('FMOD_System_SetSoftwareFormat', args=(
            ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int
        ))
        self.FMOD_System_GetSoftwareFormat = self.wrap('FMOD_System_GetSoftwareFormat', args=(
            ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)
        ))

    def wrap(self, func_name: str, args: tuple = (), res: any = ctypes.c_int) -> any:
        return super().wrap(func_name=func_name, args=args, res=res)


class FmodExMusic(backend_base.BaseMusic):
    def __init__(self, bk: any, fmod: FmodExWrapper, fp: str, mus: ctypes.c_void_p) -> None:
        super().__init__(fp)
        self.bk = bk
        self.fmod = fmod
        self.mus = mus
        self.ch = ctypes.c_void_p()
        type_buf = ctypes.c_int(0)
        bits_buf = ctypes.c_int(0)
        self.bk.check_result_warn(
            self.fmod.FMOD_Sound_GetFormat(self.mus, type_buf, None, None, bits_buf), 'Failed to get sound info'
        )
        self.type = self.fmod.format_map.get(type_buf.value) or 'none'
        self.bits = bits_buf.value
        length_buf = ctypes.c_uint(0)
        self.bk.check_result_warn(
            self.fmod.FMOD_Sound_GetLength(self.mus, length_buf, self.fmod.FMOD_TIMEUNIT_MS),
            'Failed to get sound length'
        )
        self.length = length_buf.value / 1000
        # We don't need this in the current context
        '''freq_buf = ctypes.c_float(0.0)
        self.bk.check_result_warn(self.fmod.FMOD_Sound_GetDefaults(self.mus, freq_buf, None), 'Failed to get def info')
        self.freq = freq_buf.value'''

    def play(self) -> None:
        self.bk.check_result_warn(self.fmod.FMOD_System_PlaySound(
            self.bk.sys, self.mus, None, 0, self.ch
        ), 'Failed to play music')
        freq_buf = ctypes.c_float(0.0)
        res = self.fmod.FMOD_Channel_GetFrequency(self.ch, freq_buf)
        if res == self.fmod.FMOD_OK:
            self.freq = freq_buf.value
        else:
            self.bk.check_result_warn(res, 'Failed to play music')
        pitch_buf = ctypes.c_float(0.0)
        res = self.fmod.FMOD_Channel_GetPitch(self.ch, pitch_buf)
        if res == self.fmod.FMOD_OK:
            self.pitch = pitch_buf.value
        else:
            self.bk.check_result_warn(res, 'Failed to play music')

    def stop(self) -> None:
        res = self.fmod.FMOD_Channel_Stop(self.ch)
        if res == self.fmod.FMOD_ERR_INVALID_HANDLE:
            return
        self.bk.check_result_warn(res, 'Failed to stop channel')

    def is_playing(self) -> bool:
        buf = ctypes.c_int(0)
        res = self.fmod.FMOD_Channel_IsPlaying(self.ch, buf)
        if res == self.fmod.FMOD_ERR_INVALID_HANDLE:
            return False
        self.bk.check_result_warn(res, 'Failed to get is channel playing')
        return bool(buf.value)

    def set_paused(self, paused: bool) -> None:
        res = self.fmod.FMOD_Channel_SetPaused(self.ch, paused)
        if res == self.fmod.FMOD_ERR_INVALID_HANDLE:
            return
        self.paused = paused
        self.bk.check_result_warn(res, 'Failed to set channel paused')

    def rewind(self) -> None:
        self.set_pos(0.0)

    def set_volume(self, volume: float = 1.0) -> None:
        res = self.fmod.FMOD_Channel_SetVolume(self.ch, volume)
        if res == self.fmod.FMOD_ERR_INVALID_HANDLE:
            return
        self.bk.check_result_warn(res, 'Failed to set channel volume')

    def set_speed(self, speed: float = 1.0) -> None:
        # if not self.freq:
        #     return
        # res = self.fmod.FMOD_Channel_SetFrequency(self.ch, self.freq * speed)
        res = self.fmod.FMOD_Channel_SetPitch(self.ch, self.pitch * speed)
        if res == self.fmod.FMOD_ERR_INVALID_HANDLE:
            return
        self.bk.check_result_warn(res, 'Failed to set channel speed')

    def set_pos(self, pos: float) -> None:
        res = self.fmod.FMOD_Channel_SetPosition(self.ch, int(pos * 1000), self.fmod.FMOD_TIMEUNIT_MS)
        if res == self.fmod.FMOD_ERR_INVALID_HANDLE:
            return
        self.bk.check_result_warn(res, 'Failed to set channel position')

    def get_pos(self) -> float:
        pos_buf = ctypes.c_uint(0)
        res = self.fmod.FMOD_Channel_GetPosition(self.ch, pos_buf, self.fmod.FMOD_TIMEUNIT_MS)
        if res == self.fmod.FMOD_ERR_INVALID_HANDLE:
            return 0.0
        self.bk.check_result_warn(res, 'Failed to get channel position')
        return pos_buf.value / 1000

    def destroy(self) -> None:
        if not self.fmod:
            return
        if self.mus:
            result = self.fmod.FMOD_Sound_Release(self.mus)
            if self.bk.check_result_warn:
                self.bk.check_result_warn(result, 'Failed to close music')
            self.mus = None
        self.bk = None
        self.fmod = None


class FmodExBackend(backend_base.BaseBackend):
    def __init__(self, app: any, libs: dict) -> None:
        super().__init__()
        self.title = 'FmodEx'
        self.app = app
        self.header_version = eval(app.config['fmod_version'])
        self.sys = ctypes.c_void_p()
        self.fmod = FmodExWrapper(libs.get('fmod'))
        self.device_names = []
        self.current_device_name = ''

    def init(self) -> None:
        res = self.fmod.FMOD_System_Create(self.sys, self.header_version)
        if res == self.fmod.FMOD_ERR_HEADER_MISMATCH:
            for i in range(100000000):  # Brute force
                res = self.fmod.FMOD_System_Create(self.sys, i)
                if res == self.fmod.FMOD_OK:
                    break
        self.check_result_err(res, 'Failed to create system')
        ver_buf = ctypes.c_uint()
        # TODO: fix segfault
        if 0 and self.fmod.FMOD_System_GetVersion(self.sys, ver_buf) == self.fmod.FMOD_OK \
                and not ver_buf.value == self.header_version:
            log.warn(f'Incorrect FmodEx version configured. Please change it to {hex(ver_buf.value)} in config')
        freq_buf = ctypes.c_int(41000)
        mode_buf = ctypes.c_int(0)
        channels_buf = ctypes.c_int(1)
        self.check_result_warn(self.fmod.FMOD_System_GetSoftwareFormat(
            self.sys, freq_buf, mode_buf, channels_buf
        ), 'Failed to get current audio device specs')
        if not self.app.config['freq']:
            self.app.config['freq'] = freq_buf.value
            log.warn('Please set frequency in config to', freq_buf.value)
        if not self.app.config['channels'] and channels_buf.value:
            self.app.config['channels'] = channels_buf.value
            log.warn('Please set channels in config to', channels_buf.value)
        self.check_result_warn(self.fmod.FMOD_System_SetSoftwareFormat(
            self.sys, self.app.config['freq'], mode_buf.value, self.app.config['channels']
        ), 'Failed to set audio specs')
        self.check_result_err(self.fmod.FMOD_System_Init(
            self.sys, 1, self.fmod.FMOD_INIT_THREAD_UNSAFE, None
        ), 'Failed to init system')
        if self.app.config['audio_driver']:
            if self.fmod.output_map.get(self.app.config['audio_driver']):
                self.check_result_err(self.fmod.FMOD_System_SetOutput(
                    self.sys, self.fmod.output_map.get(self.app.config['audio_driver'])
                ), 'Failed to set audio driver')
            else:
                log.warn(self.app.config['audio_driver'], 'driver not in ', self.fmod.output_map)
        num_buf = ctypes.c_int(10)
        self.check_result_warn(
            self.fmod.FMOD_System_GetNumDrivers(self.sys, num_buf), 'Failed to get audio devices number'
        )
        for i in range(num_buf.value):
            name_buf = ctypes.c_char_p(b' ' * 1024)
            self.check_result_warn(self.fmod.FMOD_System_GetDriverInfo(
                self.sys, i, name_buf, 1024, None, None, None, None
            ), 'Failed to get device info')
            if name_buf.value and name_buf.value.strip():
                self.device_names.append(self.app.bts(name_buf.value.strip()))
            else:
                self.device_names.append('')
        if self.app.config['device_name'].strip():
            if self.app.config['device_name'] in self.device_names:
                self.check_result_warn(self.fmod.FMOD_System_SetDriver(
                    self.sys, self.device_names.index(self.app.config['device_name'])
                ), 'Failed to set audio device')
            else:
                log.warn(f'Device "{self.app.config["device_name"]}" is not in devices list!')
        driver_buf = ctypes.c_int(0)
        self.check_result_warn(self.fmod.FMOD_System_GetDriver(
            self.sys, driver_buf
        ), 'Failed to get current audio device')
        try:
            self.current_device_name = self.device_names[driver_buf.value]
        except IndexError:
            self.current_device_name = ''

    def get_audio_devices_names(self) -> list:
        return self.device_names

    def get_current_audio_device_name(self) -> str:
        return self.current_device_name

    def open_music(self, fp: str) -> FmodExMusic:
        mus = ctypes.c_void_p()
        self.check_result_err(self.fmod.FMOD_System_CreateStream(
            self.sys,
            self.app.stb(fp),
            self.fmod.FMOD_LOOP_OFF | self.fmod.FMOD_2D | self.fmod.FMOD_CREATE_STREAM | self.fmod.FMOD_LOW_MEM,
            None,
            mus
        ), 'Failed to open music')
        return FmodExMusic(self, self.fmod, fp, mus)

    def quit(self) -> None:
        self.check_result_warn(self.fmod.FMOD_System_Close(self.sys), 'Failed to close system')
        self.check_result_warn(self.fmod.FMOD_System_Release(self.sys), 'Failed to release system')

    def destroy(self) -> None:
        self.sys = None
        self.fmod = None
        self.app = None

    def check_result_warn(self, result: int, error_msg: str = 'Error') -> None:
        if result == self.fmod.FMOD_OK:
            return
        log.warn(f'{error_msg} ({(self.fmod.error_map.get(result) or "Unknown error.")[:-1]})')

    def check_result_err(self, result: int, error_msg: str = 'Error') -> None:
        if result == self.fmod.FMOD_OK:
            return
        raise RuntimeError(f'{error_msg} ({(self.fmod.error_map.get(result) or "Unknown error.")[:-1]})')

    def get_audio_drivers(self) -> list:
        result = []
        if sys.platform == 'win32':
            result.append('wasapi')
            result.append('asio')
        else:
            result.append('pulseaudio')
            result.append('alsa')
        result.append('disk')
        result.append('dummy')
        return result

    def get_current_audio_driver(self) -> str:
        output_buf = ctypes.c_int(0)
        self.check_result_warn(self.fmod.FMOD_System_GetOutput(self.sys, output_buf))
        r_map = {x: k for k, x in self.fmod.output_map.items()}
        return r_map.get(output_buf.value) or 'none'

    def update(self) -> None:
        self.check_result_warn(self.fmod.FMOD_System_Update(self.sys), 'Failed to update system')
