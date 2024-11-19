from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.crud.crud_watch_later import WatchLaterDB


class WatchLaterService:
    def __init__(self, db: Session):
        self.db = db

    def add_to_watch_later(self, movie_id: int, token: dict):
        try:
            return WatchLaterDB(self.db).add_to_watch_later(movie_id, token)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    def get_watch_later(self, token: dict):
        try:
            return WatchLaterDB(self.db).get_watch_later(token)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    def delete_watch_later(self, watch_id: int, token: dict):
        try:
            return WatchLaterDB(self.db).delete_watch_later(watch_id, token)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
