import re
import json
import logging
from spotiparser.models import Track, Artist, Playlist
from spotiparser.exceptions import ScraperError
from spotiparser.utils import clean_number

logger = logging.getLogger(__name__)

class DataParser:
    def __init__(self, html: str):
        self.html = html

    def get_raw_state(self) -> dict:
        # spotify stores everything in a base64 or encoded json blob inside a script tag
        # sometimes it's 'initial-state', sometimes 'session-data'
        pattern = r'<script id="initial-state"[^>]*>([\s\S]*?)</script>'
        match = re.search(pattern, self.html)
        
        if not match:
            # try fallback for some regions
            match = re.search(r'"entities":({.*?}),"metadata"', self.html)
            if not match:
                # print(self.html) # debug print left for next time it breaks
                raise ScraperError("failed to locate hydration blob in html")
            return json.loads(match.group(0) + '}') # hacky fix for partial match
            
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError as e:
            raise ScraperError(f"broken json in script tag: {e}")

    def parse_playlist(self) -> Playlist:
        state = self.get_raw_state()
        
        # finding the actual playlist data inside their nested mess
        # FIXME: the path 'entities.items' is not stable
        try:
            root = state.get('entities', {})
            playlist_id = list(root.keys())[0] # usually the only key
            data = root[playlist_id]
            
            tracks = []
            for item in data.get('tracks', []):
                t = item.get('track', item) # sometimes nested, sometimes flat
                tracks.append(Track(
                    id=t['id'],
                    name=t['name'],
                    artists=[Artist(id=a['id'], name=a['name']) for a in t.get('artists', [])],
                    duration_ms=t.get('duration_ms', 0),
                    play_count=clean_number(t.get('playcount', '0')),
                    is_explicit=t.get('explicit', False)
                ))
            
            return Playlist(
                id=playlist_id,
                name=data.get('name', 'Unknown'),
                owner_name=data.get('owner', {}).get('name', 'Unknown'),
                tracks=tracks,
                track_count=len(tracks)
            )
        except (KeyError, IndexError) as e:
            logger.error(f"structure mismatch: {e}")
            raise ScraperError("spotify changed their internal json structure again")

def extract_play_count_from_dom(html: str) -> int:
    # backup method when json fails - look for the aria-label or specific span
    match = re.search(r'span[^>]*>([\d,]+)\s+plays</span>', html)
    if match:
        return clean_number(match.group(1))
    return 0
