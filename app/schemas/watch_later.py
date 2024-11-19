from pydantic import BaseModel


class WatchLaterBase(BaseModel):
    movie_id: int
    user_id: str
    added_at: str


class WatchLaterResponse(WatchLaterBase):
    pass
