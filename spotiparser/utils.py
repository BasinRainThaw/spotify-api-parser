import re

def clean_number(value: str) -> int:
    """Strip commas and non-digit chars from play count strings"""
    if not value:
        return 0
    cleaned = re.sub(r'[^0-9]', '', value)
    return int(cleaned) if cleaned else 0

def validate_spotify_url(url: str) -> bool:
    # very basic check, just to fail early
    patterns = [
        r'open\.spotify\.com/playlist/[a-zA-Z0-9]+',
        r'open\.spotify\.com/artist/[a-zA-Z0-9]+'
    ]
    return any(re.search(p, url) for p in patterns)
