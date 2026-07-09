from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Field

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
    cover_url: Optional[str] = None

class Playlist(BaseModel):
    id: str
    name: str
    owner_name: str
    tracks: List[Track] = Field(default_factory=list)
    track_count: int = 0
