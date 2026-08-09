import time
import random
import httpx
from spotiparser.exceptions import ConnectionError, RateLimitError

class SpotiClient:
    def __init__(self, timeout=15, retries=5):
        self.timeout = timeout
        self.retries = retries
        # randomizing user agent slightly to look less like a single bot script
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Cache-Control": "max-age=0",
        }
        self.session = httpx.Client(headers=self.headers, timeout=self.timeout, follow_redirects=True)

    def get_raw(self, url: str) -> str:
        for attempt in range(self.retries):
            try:
                # we use the same session to keep cookies between calls if needed
                resp = self.session.get(url)
                
                if resp.status_code == 429:
                    # exponential backoff with a bit of jitter
                    wait = (2 ** attempt) + random.random()
                    time.sleep(wait)
                    continue
                    
                resp.raise_for_status()
                return resp.text

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise ConnectionError(f"Not found: {url}")
                if attempt == self.retries - 1:
                    raise ConnectionError(f"HTTP {e.response.status_code} at {url}")
            except (httpx.RequestError, httpx.TimeoutException) as e:
                if attempt == self.retries - 1:
                    raise ConnectionError(f"Network fail: {e}")
                time.sleep(1)

        raise RateLimitError("Spotify is blocking us. Try again later or use a proxy.")

    def __del__(self):
        # making sure we don't leave sockets hanging
        try:
            self.session.close()
        except:
            pass
