from pydantic import BaseModel


class VideoRequest(BaseModel):
    video_key: str


class UploadVideo(BaseModel):
    filepath: str
    videoName: str
