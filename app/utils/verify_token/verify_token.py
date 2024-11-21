from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from firebase_admin import auth
from sqlalchemy.orm import Session
from app.db.models.users import User

from app.dependencies import get_db

security = HTTPBearer()


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    try:
        decoded_token = auth.verify_id_token(credentials.credentials)
        uid = decoded_token["uid"]

        try:
            user = db.query(User).filter(User.user_id == uid).first()

            decoded_token["is_admin"] = bool(user and user.is_admin)
            return decoded_token
        except Exception as db_error:
            decoded_token["is_admin"] = False
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Error en base de datos: {db_error}",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido o expirado: {str(e)}",
        )


async def is_admin(token: dict = Depends(verify_token)):
    if not token.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requieren privilegios de administrador",
        )
    return token


async def get_current_user(token: dict = Depends(verify_token)):
    """
    Dependency to get the current authenticated user.
    Works for both admin and regular users.
    """
    return token
