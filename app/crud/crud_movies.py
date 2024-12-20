from botocore.docs.bcdoc.docstringparser import PRIORITY_PARENT_TAGS
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models.movies import Movies
from app.schemas.movies import MovieUploadData


class MovieDB:
    def __init__(self, db: Session):
        self.db = db

    def upload_movie_data(self, movie: MovieUploadData, duration: int):
        try:
            db_movie = Movies(**movie.model_dump(), duration=duration)
            self.db.add(db_movie)
            self.db.commit()
            self.db.refresh(db_movie)
            return db_movie
        except HTTPException as he:
            raise HTTPException(status_code=400, detail=str(he))
        except Exception as e:
            self.db.rollback()  # Hacemos rollback en caso de error
            raise HTTPException(status_code=500, detail=str(e))

    def get_movie_name(self, skip: int, limit: int):
        try:
            db_movie = (
                self.db.query(Movies.title)
                .offset((skip - 1) * limit)
                .limit(limit)
                .all()
            )

            return [title.title for title in db_movie]

        except HTTPException as he:
            raise HTTPException(status_code=400, detail=str(he))
        except Exception as e:
            self.db.rollback()  # Hacemos rollback en caso de error
            raise HTTPException(status_code=500, detail=str(e))

    def details_movie(self, title: str):
        try:
            db_movie = self.db.query(Movies).filter(Movies.title == title).first()

            return db_movie
        except HTTPException as he:
            raise HTTPException(status_code=400, detail=str(he))
        except Exception as e:
            self.db.rollback()  # Hacemos rollback en caso de error
            raise HTTPException(status_code=500, detail=str(e))
