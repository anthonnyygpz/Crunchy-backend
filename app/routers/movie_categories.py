from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db

from app.services.movie_categories import MovieCategoriesService
from app.utils.verify_token.verify_token import is_admin

router = APIRouter()


@router.post("/api/add_to_movie_categories", tags=["movie_categories-admin"])
async def add_to_movie_categories(
    movie_id: int,
    category_id: int,
    token: dict = Depends(is_admin),
    db: Session = Depends(get_db),
):
    return MovieCategoriesService(db).add_to_movie_categories(movie_id, category_id)


@router.get("/api/get_movie_categories", tags=["movie_categories-admin"])
async def get_movie_categories(
    token: dict = Depends(is_admin), db: Session = Depends(get_db)
):
    return MovieCategoriesService(db).get_movie_categories()


@router.put("/api/update_movie_categories", tags=["movie_categories-admin"])
async def update_movie_categories(
    token: dict = Depends(is_admin), db: Session = Depends(get_db)
):
    return MovieCategoriesService(db)


@router.delete("/api/delete_movie_categories", tags=["movie_categories-admin"])
async def delete_movie_categories(
    movie_category_id: int,
    token: dict = Depends(is_admin),
    db: Session = Depends(get_db),
):
    return MovieCategoriesService(db).delete_movie_categories(movie_category_id)
