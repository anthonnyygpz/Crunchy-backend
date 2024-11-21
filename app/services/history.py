from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.crud_history import HistoryDB


class HistoryService:
    def __init__(self, db: Session):
        self.db = db

    def add_to_history(self, movie_id: int, token: dict):
        try:
            return HistoryDB(self.db).add_to_history(movie_id, token)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_history(self, token: dict):
        try:
            return HistoryDB(self.db).get_history(token)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def update_history(self, token: dict):
        try:
            return HistoryDB(self.db).update_history()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def delete_history(self, history_id: int, token: dict):
        try:
            return HistoryDB(self.db).delete_history(history_id, token)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
