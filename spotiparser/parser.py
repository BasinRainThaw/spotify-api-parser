import re
import json
from spotiparser.models import Track, Artist
from spotiparser.exceptions import ScraperError

def extract_json_blob(html: str):
    # This is brittle but works better than full html parsing for performance
    match = re.search(r'<script id="initial-state" type="text/plain">(.*?)</script>', html)
    if not match:
        raise ScraperError("Could not find initial-state script tag")
    return json.loads(match.group(1))

def parse_track(data: dict) -> Track:
    return Track(
        id=data.get('id'),
        name=data.get('name'),
        artists=[Artist(id=a['id'], name=a['name']) for a in data.get('artists', [])],
        duration_ms=data.get('duration_ms', 0)
    )
