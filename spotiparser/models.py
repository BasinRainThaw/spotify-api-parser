from typing import List, Optional
from pydantic import BaseModel, HttpUrl

class Artist(BaseModel):
    id: str
    name: str
    url: Optional[HttpUrl] = None

