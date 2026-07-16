import pytest
from spotiparser.parser import parse_spotify_state

SAMPLE_HTML = """
<html>
<body>
    <script id="initial-state" type="application/json">{"tracks": {"123": {"name": "Song A", "play_count": 5000}}}</script>
</body>
</html>
"""

def test_parse_valid_json():
    data = parse_spotify_state(SAMPLE_HTML)
    assert data["tracks"]["123"]["name"] == "Song A"

def test_parse_missing_script():
    with pytest.raises(ValueError, match="Could not find initial state"):
        parse_spotify_state("<html><body>nothing</body></html>")

