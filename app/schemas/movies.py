from typing import Optional
from botocore.validate import decimal
from pydantic import BaseModel


class VideoResponse(BaseModel):
    video_name: str


class VideoUpload(BaseModel):
    file_path: str
    video_name: str


class MovieUploadData(BaseModel):
    title: str
    description: Optional[str]
    release_year: Optional[int]
    # duration: Optional[int]
    director: Optional[str]
    # movie_name_s3: str
    thumbnail_url: Optional[str]
    rating: Optional[decimal.Decimal]
    maturity_rating: Optional[str]
    is_active: bool
