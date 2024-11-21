from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.db.models.categories import Categories
from app.schemas.categories import CreateCategoriesSchema, UpdateCategoriesSchema


class CategoriesDB:
    def __init__(self, db: Session):
        self.db = db

    def create_categories(self, category: CreateCategoriesSchema):
        try:
            db_categories = Categories(**category.model_dump())

            self.db.add(db_categories)
            self.db.commit()
            self.db.refresh(db_categories)

            return db_categories
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    def get_categories(self, category_id: int):
        try:
            db_categories = (
                self.db.query(Categories)
                .filter(Categories.category_id == category_id)
                .first()
            )
            if not db_categories:
                return "Not exits"
            return db_categories
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    def update_categories(self, category_id: int, category: UpdateCategoriesSchema):
        try:
            db_category = (
                self.db.query(Categories)
                .filter(Categories.category_id == category_id)
                .first()
            )
            if not db_category:
                raise HTTPException(status_code=404, detail="Category not exists")

            update_data = category.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_category, key, value)

            self.db.commit()
            self.db.refresh(db_category)
            return db_category
        except SQLAlchemyError as he:
            raise HTTPException(status_code=500, detail=f"Error: {str(he)}")
        # except Exception as e:
        #     raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    def delete_categories(self, category_id: int):
        try:
            db_categories = (
                self.db.query(Categories)
                .filter(Categories.category_id == category_id)
                .first()
            )

            self.db.delete(db_categories)
            self.db.commit()
            return {"message": "Delete category successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
