from typing import Optional
from botocore.validate import decimal
from pydantic import BaseModel


class MovieBase(BaseModel):
    title: str
    description: Optional[str]
    release_year: Optional[int]
    director: Optional[str]
    thumbnail_url: Optional[str]
    rating: Optional[decimal.Decimal]
    maturity_rating: Optional[str]
    is_active: bool


class MovieUploadData(MovieBase):
    pass


class MovieResponse(MovieBase):
    pass

    class Config:
        orm_mode = True
