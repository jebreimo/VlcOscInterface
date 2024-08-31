# VlcOscInterface – A simple OSC interface for VLC

This is a simple OSC interface for VLC. It allows you to control VLC via OSC messages. The interface is based on the [VLC HTTP interface](https://wiki.videolan.org/Documentation:Modules/http_intf/).

## Installation

1. Clone this repository
2. Create a virtual environment with `python -m venv .venv`
3. Install the required packages with `pip install -r requirements.txt`

## Usage

1. Activate the virtual environment with `source .venv/bin/activate`
2. Start the OSC interface with `python osc_server.py --vcl <URL to VLC>` where `<URL to VLC>` is the URL to the VLC instance you want to control. The default URL is `http://localhost:8080/requests/status.xml`.
3. Connect to the OSC interface with your OSC client
4. Send OSC messages to control VLC
5. Enjoy!

## OSC Messages

Below is a list of all the OSC messages that are supported.

- `/play` – Play or unpause the current media on the given VLC instance
- `/play <int>` – Play the media with the given index in the playlist. **Note:** the playlists themselves have indexes. If there is only one playlist, then that playlist has index 1, the "Media Library" has index 2, and the first media in the playlist has index 3.
- `/pause` – Pause or unpause the current media
- `/stop` – Stop and close the current media
- `/seek <int>` – Seek to the given time in the current media
- `/seek <int>%` – Seek to the given percentage of the total time in the current media
- `/seek +<int>` – Seek forward by the given time
- `/seek -<int>` – Seek backward by the given time
- `/fullscreen` – Toggle fullscreen mode
- `/volume <int>` – Set the volume to the given value
- `/volume <int>%` – Set the volume to the given percentage
- `/volume +<int>` – Increase the volume by the given value
- `/volume -<int>` – Decrease the volume by the given value

If the `--vlc <URL>` has been used to define multiple VLC instances, and the command should only address one of them, prefix the command with `/<number>` where `<number>` is the number of the argument, starting from 1. For instance, to pause the second VLC instance, use `/2/pause`.

## Examples

- `/play` – Play or unpause the current media
- `/play 3` – Play the first media in the playlist, assuming there is only one playlist
- `/seek 0` - Seek to the beginning of the current media
- `/1/volume 50` – Set the volume of the first VLC instance to 50%
