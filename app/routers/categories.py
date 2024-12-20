from fastapi import APIRouter, Depends
from app.dependencies import get_db
from sqlalchemy.orm import Session
from app.schemas.categories import CreateCategoriesSchema, UpdateCategoriesSchema
from app.services.categories import CategoriesService
from app.utils.verify_token.verify_token import is_admin

router = APIRouter()


@router.post("/api/create_categories", tags=["categories-admin"])
async def create_categories(
    category: CreateCategoriesSchema,
    token: dict = Depends(is_admin),
    db: Session = Depends(get_db),
):
    return CategoriesService(db).create_categories(category)


@router.get("/api/get_categories", tags=["categories-admin"])
async def get_categories(
    category_id: int, token: dict = Depends(is_admin), db: Session = Depends(get_db)
):
    return CategoriesService(db).get_categories(category_id)


@router.put("/api/update_categories", tags=["categories-admin"])
async def update_categories(
    category_id: int,
    category: UpdateCategoriesSchema,
    token: dict = Depends(is_admin),
    db: Session = Depends(get_db),
):
    return CategoriesService(db).update_categories(category_id, category)


@router.delete("/api/delete_categories", tags=["categories-admin"])
async def delete_categories(
    category_id: int, token: dict = Depends(is_admin), db: Session = Depends(get_db)
):
    return CategoriesService(db).delete_categories(category_id)
