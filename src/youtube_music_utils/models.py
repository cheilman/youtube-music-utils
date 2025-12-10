from dataclasses import dataclass
from datetime import timedelta
from typing import Optional


@dataclass
class SongDetails:
    title: str
    artist: str
    video_id: str
    length: timedelta
    album: Optional[str] = None
