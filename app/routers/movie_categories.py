from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db

from app.services.movie_categories import MovieCategoriesService

router = APIRouter()


@router.post("/api/add_to_movie_categories", tags=["movie_categories"])
async def add_to_movie_categories(
    movie_id: int, category_id: int, db: Session = Depends(get_db)
):
    return MovieCategoriesService(db).add_to_movie_categories(movie_id, category_id)


@router.get("/api/get_movie_categories", tags=["movie_categories"])
async def get_movie_categories(db: Session = Depends(get_db)):
    return MovieCategoriesService(db).get_movie_categories()


@router.put("/api/update_movie_categories", tags=["movie_categories"])
async def update_movie_categories(db: Session = Depends(get_db)):
    return MovieCategoriesService(db)


@router.delete("/api/delete_movie_categories", tags=["movie_categories"])
async def delete_movie_categories(
    movie_category_id: int, db: Session = Depends(get_db)
):
    return MovieCategoriesService(db).delete_movie_categories(movie_category_id)
