# MUST
Simple Terminal Music Player (Server/Client), written in python <br />
I made it mostly for myself because there is no foobar2000 on linux
## Supported Audio Backends
 - SDL2/SDL2_mixer
 - FmodEx
## Supported Communication Backends
 - TCP Sockets via threading.Thread
## How does it work?
By default, it tries to run itself as a server.
If it fails, it tries to connect as a client. <br />
It has two playlists: main and temp.
It picks tracks from temp playlist until it has them, then it will play main playlist
Main playlist should be specified by `music_path` var in config or via cmdline args (for ease of use with file managers). <br />
Client can send commands to the server (currently can't receive).
You can run client with cmdline args to send and without, to enter command prompt mode.
In prompt mode, commands can be split by `;`
## Example Commands
```shell
# First Terminal (Server)
python main.py --server-only  # optional arg, to fail if can't start the server
# Seconds Terminal (Client)
python main.py next  # next track
python main.py toggle_pause  # pause/resume track
# for volume, speed, pos_sec (seconds), pos_rel (in % like with volume)
python main.py "volume 0.5"  # set volume to 50%
python main.py "volume_ch 0.1"  # add +10% to volume
python main.py "volume_ch -0.1"  # add -10% to volume
python main.py music1.mp3 "m u s i c 2.mp3"  # add files to the temp playlist
python main.py clear_temp  # clear temp playlist
python main.py  # Enter Prompt Mode
>>> volume 0.5; next; speed 2.0
>>> disconnect  # Just Disconnect
python main.py exit  # Terminate
```