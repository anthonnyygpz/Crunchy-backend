from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models.movies import Movie
from app.schemas.movies import MovieUploadData


class MovieDB:
    def __init__(self, db: Session):
        self.db = db

    def upload_movie_data(self, movie: MovieUploadData, duration: int):
        try:
            db_movie = Movie(**movie.model_dump(), duration=duration)
            self.db.add(db_movie)
            self.db.commit()
            self.db.refresh(db_movie)
            return db_movie
        except HTTPException as he:
            raise HTTPException(status_code=400, detail=str(he))
        except Exception as e:
            self.db.rollback()  # Hacemos rollback en caso de error
            raise HTTPException(status_code=500, detail=str(e))
