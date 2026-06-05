import time
import httpx
from spotiparser.exceptions import ConnectionError, RateLimitError

class SpotiClient:
    """
    Handles HTTP requests to Spotify with some basic spoofing
    to avoid immediate blocks.
    """
    def __init__(self, timeout=10, retries=3):
        self.timeout = timeout
        self.retries = retries
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        }

    def get_raw(self, url: str) -> str:
        attempt = 0
        while attempt < self.retries:
            try:
                with httpx.Client(headers=self.headers, timeout=self.timeout) as client:
                    resp = client.get(url)
                    
                    if resp.status_code == 429:
                        # spotify is grumpy
                        wait = (attempt + 1) * 2
                        time.sleep(wait)
                        attempt += 1
                        continue
                        
                    resp.raise_for_status()
                    return resp.text
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise ConnectionError(f"Resource not found: {url}")
                raise ConnectionError(f"HTTP error: {e.response.status_code}")
            except httpx.RequestError as e:
                attempt += 1
                if attempt == self.retries:
                    raise ConnectionError(f"Failed after {self.retries} attempts: {e}")

        raise RateLimitError("Backing off after too many 429s")

    def get_json(self, url: str):
        # some internal spotify endpoints return pure json
        # we might need this for some deeper scraping
        data = self.get_raw(url)
        import json
        return json.loads(data)
