from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_db
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from firebase_admin import auth

from app.schemas.user import UserCreate, UserUpdate, UserLogin
from app.services.user import UserService, UserServiceDB
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()


router = APIRouter()
security = HTTPBearer()


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        decoded_token = auth.verify_id_token(credentials.credentials)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido o expirado: {str(e)}",
        )


@router.post(
    "/api/register_users",
    response_model=UserCreate,
    summary="Crear usuarios",
    description="Registrar usuarios con autenticación",
    tags=["users"],
)
async def create_user(user: UserCreate, password: str, db: Session = Depends(get_db)):
    return UserServiceDB(db).create_user(user, password)


@router.get(
    "/api/get_user_current_data",
    summary="Obtener los datos del usuario.",
    description="Obtiene todo datos del usuario.",
    tags=["users"],
)
async def get_user_current_data(
    token: dict = Depends(verify_token), db: Session = Depends(get_db)
):
    return UserServiceDB(db).get_user_current_data(token)


@router.put(
    "/api/update_users/",
    summary="Actualizar datos del usuario.",
    description="Aquí se le asigna el nombre al usuario",
    tags=["users"],
)
async def update_user(
    user: UserUpdate, token: dict = Depends(verify_token), db: Session = Depends(get_db)
):
    return UserServiceDB(db).update_user(user, token)


@router.delete(
    "/api/delete_users/",
    summary="Borrar usuario",
    description="Borrar al usuario",
    tags=["users"],
)
async def delete_user(
    token: dict = Depends(verify_token), db: Session = Depends(get_db)
):
    return UserServiceDB(db).delete_user(token)


@router.post(
    "/api/password_reset/{email}",
    summary="Reiniciar contraseña",
    description="Envia un a tu correo un link para cambiar la contraseña.",
    tags=["users"],
)
async def password_reset(email: str):
    return UserService().password_reset(email)


@router.post("/api/refresh-token/", tags=["users"])
async def refresh_token(refresh_token: str):
    return UserService().refresh_token(refresh_token)


@router.post(
    "/api/login/",
    summary="Iniciar sesion",
    description="Se inicia sesion con el token generado.",
    tags=["users"],
)
async def login(user: UserLogin):
    return UserService().login(user)


@router.post(
    "/api/logout/",
    summary="Cerrar sesion.",
    description="Se cierra la sesion del token.",
    tags=["users"],
)
async def logout(token: dict = Depends(verify_token)):
    return UserService().logout(token)


# @router.post("/api/verify_email/", tags=["users"])
# async def verify_email(token: str):
#     return UserService().verify_email(token)
