from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.history import History
from sqlalchemy.orm import joinedload


class HistoryDB:
    def __init__(self, db: Session):
        self.db = db

    def add_to_history(self, movie_id: int, token: dict):
        try:
            db_history = (
                self.db.query(History)
                .options(joinedload(History.movies))  # Hacemos el join con movies
                .filter(
                    History.movie_id == movie_id, History.user_id == token["user_id"]
                )
                .first()
            )

            if not db_history:
                db_history = History(
                    movie_id=movie_id,
                    user_id=token["user_id"],
                )
                self.db.add(db_history)
                self.db.commit()
                self.db.refresh(db_history)

                # Recargamos el objeto con los datos de movies
                db_history = (
                    self.db.query(History)
                    .options(joinedload(History.movies))
                    .filter(History.user_id == db_history.user_id)
                    .first()
                )

            return db_history
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_history(self, token: dict):
        try:
            # Consultamos el historial con joins a movies
            db_history = (
                self.db.query(History)
                .options(joinedload(History.movies))  # Join con movies
                .filter(History.user_id == token["user_id"])
                .order_by(History.watch_date.desc())
                .all()
            )
            return db_history
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def update_history(self):
        try:
            pass
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def delete_history(self, history_id: int, token: dict):
        try:
            db_history = self.db.query(History).filter(
                History.history_id == history_id,
                History.user_id == token["user_id"].all(),
            )
            if not db_history:
                raise HTTPException(status_code=404, detail="History not found")

            self.db.delete(db_history)
            self.db.commit()
            return {"message": "History remove successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
