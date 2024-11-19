from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models.watch_later import WatchLater


class WatchLaterDB:
    def __init__(self, db: Session):
        self.db = db

    def add_to_watch_later(self, movie_id: int, token: dict):
        try:
            db_watch_later = WatchLater(movie_id=movie_id, user_id=token["user_id"])
            self.db.add(db_watch_later)
            self.db.commit()
            self.db.refresh(db_watch_later)
            return db_watch_later
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_watch_later(self, token: dict):
        try:
            db_watch_later = (
                self.db.query(WatchLater)
                .filter(WatchLater.user_id == token["user_id"])
                .all()
            )
            return db_watch_later
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def delete_watch_later(self, watch_id: int, token: dict):
        try:
            db_watch_later = (
                self.db.query(WatchLater)
                .filter(
                    WatchLater.watch_id == watch_id
                    and WatchLater.user_id == token["user_id"]
                )
                .first()
            )
            self.db.delete(db_watch_later)
            self.db.commit()
            return {"message": "Deleted watch later successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
