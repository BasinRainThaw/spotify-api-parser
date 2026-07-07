BASE_URL = "https://open.spotify.com"

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# we need this to find the hydrated state in the html source
STATE_RE = r'<script id="initial-state" type="application/json">(.*?)</script>'

TRACK_ID_RE = r"spotify:track:([a-zA-Z0-9]{22})"
PLAYLIST_ID_RE = r"spotify:playlist:([a-zA-Z0-9]{22})"

# sometimes spotify uses a different script tag id depending on the region/rollout
# TODO: check if 'session-state' is ever used instead of 'initial-state'
