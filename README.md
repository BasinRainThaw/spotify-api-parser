# spotify-api-parser

Just a quick tool to grab track info from public Spotify links. I got tired of the official API's rate limits and auth overhead when I just wanted to dump some playlist metadata to JSON.

It uses a mix of internal web API endpoints and some regex on the raw HTML where the JSON payload is embedded. It's fragile and will probably break when Spotify changes their frontend, but it works for now.

## Setup

Needs Python 3.10+.

```bash
pip install -e .
```

## Usage

Pass a playlist or album URL:

```bash
spotify-parser https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoPBqpw
```

Or use it in code:

```python
from spotiparser import fetch_playlist

data = fetch_playlist("playlist_id")
for track in data['tracks']:
    print(f"{track['name']} - {track['artist']}")
```

## License
MIT
