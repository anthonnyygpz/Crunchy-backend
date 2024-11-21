from app.dependencies import get_db
from app.schemas.user import UserCreate, UserLogin, UserUpdate
from app.services.user import UserService, UserServiceDB
from app.utils.verify_token.verify_token import is_admin, verify_token
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

load_dotenv()


router = APIRouter()


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
    token: dict = Depends(is_admin), db: Session = Depends(get_db)
):
    return UserServiceDB(db).get_user_current_data(token)


@router.put(
    "/api/update_users/",
    summary="Actualizar datos del usuario.",
    description="Aquí se le asigna el nombre al usuario",
    tags=["users"],
)
async def update_user(
    user: UserUpdate, token: dict = Depends(is_admin), db: Session = Depends(get_db)
):
    return UserServiceDB(db).update_user(user, token)


@router.delete(
    "/api/delete_users/",
    summary="Borrar usuario",
    description="Borrar al usuario",
    tags=["users"],
)
async def delete_user(token: dict = Depends(is_admin), db: Session = Depends(get_db)):
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
async def logout(token: dict = Depends(is_admin)):
    return UserService().logout(token)


@router.post("/api/verify_email/", tags=["users"])
async def verify_email(token: str):
    return UserService().verify_email(token)


# @router.get("/ruta_admin")
# async def ruta_admin(token: dict = Depends(is_admin)):
#     # Solo accesible para admins
#     # print(token)
#     return {"mensaje": "Acceso de administrador concedido"}
