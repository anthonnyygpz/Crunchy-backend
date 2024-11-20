from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.crud.crud_categories import CategoriesDB
from app.schemas.categories import CreateCategoriesSchema, UpdateCategoriesSchema


class CategoriesService:
    def __init__(self, db: Session):
        self.db = db

    def create_categories(
        self,
        category: CreateCategoriesSchema,
    ):
        try:
            return CategoriesDB(self.db).create_categories(category)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

    def get_categories(self, category_id: int):
        try:
            return CategoriesDB(self.db).get_categories(category_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

    def update_categories(self, category_id: int, category: UpdateCategoriesSchema):
        try:
            return CategoriesDB(self.db).update_categories(category_id, category)

        except SQLAlchemyError as he:
            raise HTTPException(status_code=500, detail=f"Error: {str(he)}")
        # except Exception as e:
        #     raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

    def delete_categories(self, category_id: int):
        try:
            return CategoriesDB(self.db).delete_categories(category_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
