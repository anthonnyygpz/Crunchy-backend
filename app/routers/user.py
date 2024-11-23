from app.dependencies import get_db
from app.schemas.user import UserCreate, UserLogin, UserUpdate
from app.services.user import UserService, UserServiceDB
from app.utils.verify_token.verify_token import get_current_user
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

load_dotenv()


router = APIRouter(
    prefix="/api",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/register_users",
    response_model=UserCreate,
)
async def create_user(user: UserCreate, password: str, db: Session = Depends(get_db)):
    """
    Registra el usuario en la base de datos con los siguiente datos:
    - **email**: Es el correo que se usara para crear la cuenta (Obligatorio).
    - **username**: Es el nombre el usuario que solo se le mostrara al usuario (Opcional).
    - **first_name**: Es el nombre(s) del usuario (Obligatorio).
    - **first_last_name**: Es el primer apellido o apellido paterno (Opcional).
    - **second_last_name**: Es el segundo apellido o apellido materno (Obligatorio).
    - **profile_picture_url**: Es la url de la imagen que se usara (Opcional).
    """
    return UserServiceDB(db).create_user(user, password)


@router.get(
    "/get_user_current_data",
)
async def get_user_current_data(
    token: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Obtiene todo los datos del usuario:
    """

    return UserServiceDB(db).get_user_current_data(token)


@router.put(
    "/update_users/",
    summary="Actualizar datos del usuario.",
    description="Aquí se le asigna el nombre al usuario",
    tags=["users"],
)
async def update_user(
    user: UserUpdate,
    token: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return UserServiceDB(db).update_user(user, token)


@router.delete(
    "/delete_users/",
    summary="Borrar usuario",
    description="Borrar al usuario",
    tags=["users"],
)
async def delete_user(
    token: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    return UserServiceDB(db).delete_user(token)


@router.post(
    "/password_reset/{email}",
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
    "/login/",
    summary="Iniciar sesion",
    description="Se inicia sesion con el token generado.",
    tags=["users"],
)
async def login(user: UserLogin):
    return UserService().login(user)


@router.post(
    "/logout/",
    summary="Cerrar sesion.",
    description="Se cierra la sesion del token.",
    tags=["users"],
)
async def logout(token: dict = Depends(get_current_user)):
    return UserService().logout(token)


@router.post("/verify_email/", tags=["users"])
async def verify_email(token: str = Depends(get_current_user)):
    return UserService().verify_email(token)
