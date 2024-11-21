from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.utils.verify_token.verify_token import get_current_user
from app.dependencies import get_db
from app.services.watch_later import WatchLaterService

router = APIRouter()


@router.post("/api/add_to_watch_later", tags=["watch_later"])
async def add_to_watch_later(
    movie_id: int,
    token: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return WatchLaterService(db).add_to_watch_later(movie_id, token)


@router.get("/api/get_watch_later", tags=["watch_later"])
async def get_watch_later(
    token: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    return WatchLaterService(db).get_watch_later(token)


@router.delete("/api/update_watch_later", tags=["watch_later"])
async def delete_watch_later(
    watch_id: int,
    token: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return WatchLaterService(db).delete_watch_later(watch_id, token)
