from typing import List, Optional
from pydantic import BaseModel, HttpUrl

class Artist(BaseModel):
    id: str
    name: str
    url: Optional[HttpUrl] = None

class Track(BaseModel):
    id: str
    name: str
    artists: List[Artist]
    duration_ms: int
    play_count: Optional[int] = 0
    is_explicit: bool = False
    album_name: Optional[str] = None
