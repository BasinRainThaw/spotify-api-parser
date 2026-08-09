import time
import asyncio
import statistics
from spotiparser.client import SpotifyClient

# some are huge to stress test the chunking
TEST_PLAYLISTS = [
    "37i9dQZF1DXcBWIGoYBM5M",
    "37i9dQZF1DX0XUsKBvIYmg",
    "37i9dQZF1DX4JAvHpj5Zsb",
    "37i9dQZF1DX4dyzvS6S4Ym",
    "37i9dQZF1DWTo8o2REq9MT"
]

async def bench_playlist(client, pid):
    t0 = time.perf_counter()
    try:
        tracks = await client.get_playlist_tracks(pid)
        elapsed = time.perf_counter() - t0
        return len(tracks), elapsed
    except Exception as e:
        print(f"failed {pid}: {e}")
        return 0, 0

async def main():
    """Simple runner to see if we're hitting bottlenecking or local overhead."""
    client = SpotifyClient(timeout=30)
    print(f"starting benchmark on {len(TEST_PLAYLISTS)} playlists...")
    
    start_time = time.perf_counter()
    
    # don't want to spam too hard or we'll get 429 even without the api
    tasks = [bench_playlist(client, p) for p in TEST_PLAYLISTS]
    results = await asyncio.gather(*tasks)
    
    total_time = time.perf_counter() - start_time
    
    counts = [r[0] for r in results if r[0] > 0]
    times = [r[1] for r in results if r[1] > 0]
    
    if not times:
        print("all requests failed")
        return

    print("\n--- results ---")
    print(f"total tracks: {sum(counts)}")
    print(f"avg time per playlist: {statistics.mean(times):.2f}s")
    print(f"fastest: {min(times):.2f}s")
    print(f"slowest: {max(times):.2f}s")
    print(f"total wall time: {total_time:.2f}s")
    # print(f"tracks per second: {sum(counts) / total_time:.1f}") 

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
