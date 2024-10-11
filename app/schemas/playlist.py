from pydantic import BaseModel


class CreatePlaylist(BaseModel):
    createdBy: str
    isPublic: bool
    tumbnailUrl: str
    title: str
    videoCount: int
    videoId: int
