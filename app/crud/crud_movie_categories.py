from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.movie_categories import MovieCategories


class MovieCategoriesDB:
    def __init__(self, db: Session):
        self.db = db

    def add_to_movie_categories(self, movie_id: int, category_id: int):
        try:
            db_movie_categories = MovieCategories(
                movie_id=movie_id, category_id=category_id
            )

            self.db.add(db_movie_categories)
            self.db.commit()
            self.db.refresh(db_movie_categories)

            return db_movie_categories
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_movie_categories(self):
        try:
            # db_movie_categories = self.db.query(MovieCategories).all()
            db_movie_categories = (
                self.db.query(MovieCategories)
                .order_by(MovieCategories.category_id)
                .all()
            )
            return db_movie_categories

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def update_movie_categories(self):
        try:
            pass
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def delete_movie_categories(self, movie_category_id: int):
        try:
            db_movie_categories = (
                self.db.query(MovieCategories)
                .filter(MovieCategories.movie_category_id == movie_category_id)
                .first()
            )

            if db_movie_categories is None:
                raise HTTPException(status_code=404, detail="Category not found")
            self.db.delete(db_movie_categories)
            self.db.commit()

            return {"message": "Movie category delete successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
