class SpotiparserError(Exception):
    """Base exception for everything here"""
    pass

class RateLimitError(SpotiparserError):
    def __init__(self, message="Spotify is blocking us (429)", retry_after=None):
        self.retry_after = retry_after
        super().__init__(message)

