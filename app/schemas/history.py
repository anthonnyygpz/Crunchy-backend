from pydantic import BaseModel


class HistoryBase(BaseModel):
    user_id: str
    movie_id: int


class ResponseHistorySchema(HistoryBase):
    history_id: int
    watch_duration: int
    completed: bool
    last_position: int


class UpdateHistorySchema(HistoryBase):
    watch_date: str
    watch_duration: int
    completed: bool
    last_position: int
