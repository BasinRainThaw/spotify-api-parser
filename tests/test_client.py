import pytest
import respx
from httpx import Response
from spotiparser.client import SpotifyClient

@respx.mock
@pytest.mark.asyncio
async def test_get_playlist_success():
    client = SpotifyClient()
    route = respx.get("https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M").mock(
        return_value=Response(200, content='<script id="initial-state" type="application/json">{"data": "ok"}</script>')
    )
    
    res = await client.get_playlist("37i9dQZF1DXcBWIGoYBM5M")
    assert route.called
    assert res == {"data": "ok"}

@respx.mock
@pytest.mark.asyncio
async def test_retry_on_429():
    client = SpotifyClient(retries=1)
    # first call 429, second 200
    route = respx.get("https://open.spotify.com/playlist/123").side_effect = [
        Response(429),
        Response(200, content='<script id="initial-state" type="application/json">{"retry": "worked"}</script>')
    ]
    
    # print("debugging retries...") # left this here to check why it was failing on CI
    res = await client.get_playlist("123")
    assert res["retry"] == "worked"
