from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.services.movies import VideoServiceDB
from app.schemas.movies import MovieUploadData, VideoResponse

router = APIRouter()


@router.post(
    "/api/uploads",
    # response_model=Mov,
    summary="Subir videos.",
    description="Almacena los videos para mostrar en la aplicacion web.",
    tags=["movies"],
)
async def uploads(
    movie: MovieUploadData, file_path: str, db: Session = Depends(get_db)
):
    return VideoServiceDB(db).uploads(movie, file_path)


@router.get(
    "/api/get_videos_name",
    response_model=dict,
    summary="Listar los videos.",
    description="Lista todo los video que hay almacenados.",
    tags=["movies"],
)
async def get_videos_name(db: Session = Depends(get_db)):
    return VideoServiceDB(db).get_videos_name()


@router.get(
    "/api/generate_urls/{video_name}",
    response_model=VideoResponse,
    summary="Obtener la url.",
    description="Genera la url que mostrara la url del video.",
    tags=["movies"],
)
async def generate_urls(video_name: str, db: Session = Depends(get_db)):
    return VideoServiceDB(db).generate_urls(video_name)
