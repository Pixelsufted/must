# MUST
Simple Terminal Music Player (Server/Client), written in python <br />
I made it mostly for myself because there is no foobar2000 on linux
## Supported Audio Backends
 - Windows MultiMedia Library
 - SDL2/SDL2_mixer
 - FmodEx
## Supported Communication Backends
 - TCP Sockets via threading.Thread
 - UDP Sockets (Single-Threaded) via threading.Thread
## How does it work?
It has simple structure, so you can easily modify the code for your need.
For example, I added [Waybar](https://github.com/Alexays/Waybar) support in the code via `print_json` var in config. <br />
By default, it tries to run itself as a server.
If it fails, it tries to connect as a client. <br />
It has two playlists: main and temp.
It picks tracks from temp playlist until it has them, then it will play main playlist.
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
## Example Waybar Configuration
Note: disable logging and enable json print in config
```json
"custom/media": {
    "format": "{}",
    "return-type": "json",
    "max-length": 100,
    "escape": true,
    "exec": "python /home/lexa/Documents/must/main.py --server-only 2> /dev/null"
}
```

## Example DWL Binds
```c
/* commands */
static const char *next_player_cmd[] = { "python", "/home/lexa/Documents/must/main.py", "--client-only", "next", NULL };
static const char *pause_player_cmd[] = { "python", "/home/lexa/Documents/must/main.py", "--client-only", "toggle_pause", NULL };
static const char *vol_add_cmd[] = { "python", "/home/lexa/Documents/must/main.py", "--client-only", "volume_ch 0.05", NULL };
static const char *vol_sub_cmd[] = { "python", "/home/lexa/Documents/must/main.py", "--client-only", "volume_ch -0.05", NULL };
static const char *pos_add_cmd[] = { "python", "/home/lexa/Documents/must/main.py", "--client-only", "pos_sec_ch 10", NULL };
static const char *pos_sub_cmd[] = { "python", "/home/lexa/Documents/must/main.py", "--client-only", "pos_sec_ch -10", NULL };
static const char *rewind_cmd[] = { "python", "/home/lexa/Documents/must/main.py", "--client-only", "rewind", NULL };

static const Key keys[] = {
	/* modifier                  key                 function        argument */
    /* ...  Other Keys ... */
	{ 0,                         XKB_KEY_KP_Down,          spawn,          {.v = next_player_cmd} },
	{ 0,                         XKB_KEY_KP_Begin,          spawn,          {.v = pause_player_cmd} },
	{ 0,                         XKB_KEY_KP_End,          spawn,          {.v = pos_sub_cmd} },
	{ 0,                         XKB_KEY_KP_Next,          spawn,          {.v = pos_add_cmd} },
	{ 0,                         XKB_KEY_KP_Left,          spawn,          {.v = vol_sub_cmd} },
	{ 0,                         XKB_KEY_KP_Right,          spawn,          {.v = vol_add_cmd} },
	{ 0,                         XKB_KEY_KP_Up,          spawn,          {.v = rewind_cmd} }
};
```

## Example Someblocks Configuration
Note: enable someblocks_support in config and set current_music_info_path to /dev/shm/must_music_info

```c
// Singal 10 is hardcoded in main.py
static const Block blocks[] = {
	/*Icon*/	/*Command*/		/*Update Interval*/	/*Update Signal*/	
	{"", "cat /dev/shm/must_music_info",					0,		10},
	{"", "date '+%b %d (%a) %I:%M%p'",					5,		0},
};
```
