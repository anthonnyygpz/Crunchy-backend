from typing import Optional
from pydantic import BaseModel


class CategoriesBase(BaseModel):
    name: str
    description: Optional[str] = None


class CreateCategoriesSchema(CategoriesBase):
    pass


class RespnseCategoriesSchema(CategoriesBase):
    categori_id: int
    is_active: bool

    class Config:
        from_attributes = True


class UpdateCategoriesSchema(BaseModel):
    # name: str | None = None
    # description: str | None = None
    # is_active: bool | None = None
    name: Optional["str"]
    description: Optional["str"]
    is_active: Optional["bool"]

    class Config:
        from_attributes = True
