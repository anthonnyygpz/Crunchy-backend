from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.services.movies import MovieServiceDB
from app.schemas.movies import MovieUploadData, MovieResponse
from app.utils.verify_token.verify_token import get_current_user, is_admin

router = APIRouter(
    prefix="/api",
    tags=["movies-admin"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/uploads",
    # response_model=Mov,
    summary="Subir videos.",
    description="Almacena los videos para mostrar en la aplicacion web.",
    tags=["movies-admin"],
)
async def uploads(
    movie: MovieUploadData,
    file_path: str,
    token: dict = Depends(is_admin),
    db: Session = Depends(get_db),
):
    return MovieServiceDB(db).uploads(movie, file_path)


@router.get(
    "/get_videos_name",
    # response_model=dict,
    summary="Listar los videos.",
    description="Lista todo los video que hay almacenados.",
)
async def get_videos_name(
    skip: int = 1,
    limit: int = 100,
    token: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return MovieServiceDB(db).get_videos_name(skip, limit)


@router.get(
    "/generate_urls/{video_name}",
    response_model=MovieResponse,
    summary="Obtener la url.",
    description="Genera la url que mostrara la url del video.",
    tags=["movies-admin"],
)
async def generate_urls(
    video_name: str, token: dict = Depends(is_admin), db: Session = Depends(get_db)
):
    return MovieServiceDB(db).generate_urls(video_name)


@router.get(
    "/details_movie",
    summary="Detalles de las peliculas",
    description="Obtiene los detalles de las peliculas.",
    tags=["movies-admin"],
)
async def details_movie(
    title: str, token: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    return MovieServiceDB(db).details_movie(title)
