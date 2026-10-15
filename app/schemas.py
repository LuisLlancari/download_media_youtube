from pydantic import BaseModel

class InfoRequest(BaseModel):
  url: str

class AudioRequest(BaseModel):
  url: str
  bitrate: str = "192"  # "128", "192", "320"
  title: str | None = None

class VideoRequest(BaseModel):
  url: str
  quality: str = "720"  # "1080", "720", "480", "360", etc.
  title: str | None = None