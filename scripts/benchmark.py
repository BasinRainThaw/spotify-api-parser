import time
import asyncio
from spotiparser.client import SpotifyClient

# testing with some massive public playlists
TARGETS = [
    "37i9dQZF1DXcBWIGoYBM5M", # Todays Top Hits
    "37i9dQZF1DX0XUsKBvIYmg", # New Music Friday
]

async def run_bench():
    client = SpotifyClient()
    start = time.perf_counter()
    
    for playlist_id in TARGETS:
        print(f"fetching {playlist_id}...")
        tracks = await client.get_playlist_tracks(playlist_id)
        print(f"got {len(tracks)} tracks")

    end = time.perf_counter()
    print(f"total time: {end - start:.2f}s")

if __name__ == "__main__":
    asyncio.run(run_bench())
