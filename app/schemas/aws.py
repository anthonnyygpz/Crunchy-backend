from pydantic import BaseModel


class VideoRequest(BaseModel):
    video_key: str