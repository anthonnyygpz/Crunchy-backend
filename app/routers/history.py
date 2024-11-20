from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.utils.verify_token.verify_token import verify_token

from app.services.history import HistoryService

router = APIRouter()


@router.post("/api/add_to_history", tags=["history"])
async def add_to_history(
    movie_id: int,
    token: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):
    return HistoryService(db).add_to_history(movie_id, token)


@router.get("/api/get_history", tags=["history"])
async def get_history(
    token: dict = Depends(verify_token), db: Session = Depends(get_db)
):
    return HistoryService(db).get_history(token)


@router.put("/api/update_history", tags=["history"])
async def update_history(
    token: dict = Depends(verify_token), db: Session = Depends(get_db)
):
    return HistoryService(db).update_history(token)


@router.delete("/api/delete_history", tags=["history"])
async def delete_history(
    history_id: int, token: dict = Depends(verify_token), db: Session = Depends(get_db)
):
    return HistoryService(db).delete_history(history_id, token)
