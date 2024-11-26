from app.dependencies import get_db
from app.schemas.user import CreateUserSchema, LoginUserSchema, UpdateUserSchema
from app.services.user import UserService, UserServiceDB
from app.utils.verify_token.verify_token import get_current_user
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/api",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register_users")
async def create_user(user: CreateUserSchema, db: Session = Depends(get_db)):
    """
    Registra el usuario en la base de datos con los siguiente datos:
    - **email**: Es el correo que se usara para crear la cuenta (Obligatorio).
    - **username**: Es el nombre el usuario que solo se le mostrara al usuario (Opcional).
    - **first_name**: Es el nombre(s) del usuario (Obligatorio).
    - **first_last_name**: Es el primer apellido o apellido paterno (Opcional).
    - **second_last_name**: Es el segundo apellido o apellido materno (Obligatorio).
    - **profile_picture_url**: Es la url de la imagen que se usara (Opcional).
    """
    return UserServiceDB(db).create_user(user)


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
    "/update_users",
)
async def update_user(
    user: UpdateUserSchema,
    token: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Actualiza los datos de la base de datos con lo siguientes datos:
    - **username**: Es el nombre el usuario que solo se le mostrara al usuario.
    - **first_name**: Es el nombre(s) del usuario.
    - **first_last_name**: Es el primer apellido o apellido paterno.
    - **second_last_name**: Es el segundo apellido o apellido materno.
    - **profile_picture_url**: Es la url de la imagen que se usara.
    - **is_active**: bool
    """
    return UserServiceDB(db).update_user(user, token)


@router.delete("/delete_users")
async def delete_user(
    token: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Se elimina al usuario de la base de datos:
    """
    return UserServiceDB(db).delete_user(token)


@router.post("/password_reset")
async def password_reset(email: str):
    """
    Se envia a tu correo un link para reiniciar tu contraseña:
    - **email**: Es un correo electronico que que si exista (Obligatorio).
    """
    return UserService().password_reset(email)


@router.post("/refresh-token")
async def refresh_token(refresh_token: str):
    """
    Vulve a refrescar el token para que no se tenga que volver a inicar sesion:
    - **refresh-token**: Es el refresh_token que se genera al momento de iniciar sesion (Obligatorio).

    """
    return UserService().refresh_token(refresh_token)


@router.post("/login")
async def login(user: LoginUserSchema):
    """
    Inicia sesion generando un token y un refresh_token con lo sigueintes datos:
    - **email**: Es el correo electronico que se usara para iniciar sesion (Obligatorio).
    - **password**: Es la contraseña que se usara para iniciar sesion (Obligatorio).
    """
    return UserService().login(user)


@router.post("/logout")
async def logout(token: dict = Depends(get_current_user)):
    """
    Cierra sesion del usuario.
    """
    return UserService().logout(token)


@router.post("/verify_email")
async def verify_email(token: str = Depends(get_current_user)):
    """
    Se envia un link al correo para verificar la cuenta.
    """
    return UserService().verify_email(token)

