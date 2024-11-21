from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.crud_movie_categories import MovieCategoriesDB


class MovieCategoriesService:
    def __init__(self, db: Session):
        self.db = db

    def add_to_movie_categories(self, movie_id: int, category_id: int):
        try:
            return MovieCategoriesDB(self.db).add_to_movie_categories(
                movie_id, category_id
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_movie_categories(self):
        try:
            return MovieCategoriesDB(self.db).get_movie_categories()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def update_movie_categories(self):
        try:
            return MovieCategoriesDB(self.db).update_movie_categories()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def delete_movie_categories(self, movie_category_id: int):
        try:
            return MovieCategoriesDB(self.db).delete_movie_categories(movie_category_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
