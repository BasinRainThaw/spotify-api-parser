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
    # we use a very short backoff in tests to avoid slowing down the suite
    client = SpotifyClient(retries=1, backoff_factor=0.01)
    
    url = "https://open.spotify.com/playlist/123"
    respx.get(url).side_effect = [
        Response(429),
        Response(200, content='<script id="initial-state" type="application/json">{"retry": "worked"}</script>')
    ]
    
    res = await client.get_playlist("123")
    assert res["retry"] == "worked"

@respx.mock
@pytest.mark.asyncio
async def test_handle_not_found():
    client = SpotifyClient()
    respx.get("https://open.spotify.com/playlist/missing").mock(return_value=Response(404))
    
    with pytest.raises(RuntimeError, match="404"):
        await client.get_playlist("missing")
