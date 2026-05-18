BASE_URL = "https://open.spotify.com"

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# we need this to find the hydrated state in the html source
STATE_RE = r'<script id="initial-state" type="application/json">(.*?)</script>'
