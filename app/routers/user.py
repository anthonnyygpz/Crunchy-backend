from fastapi import APIRouter, Depends
from app.dependencies import get_db
from sqlalchemy.orm import Session


from app.schemas.user import UserResponse, UserCreate, UserUpdate
from app.services.user import UserService, UserServiceDB

router = APIRouter()


@router.post(
    "/users/",
    response_model=UserResponse,
    summary="Crear usuarios",
    description="Registrar usuarios con autenticación",
    tags=["users"],
)
async def create_user(user: UserCreate, password: str, db: Session = Depends(get_db)):
    return UserServiceDB(db).create_user(user, password)


@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Obtener los datos del usuario.",
    description="Obtiene todo datos del usuario.",
    tags=["users"],
)
async def read_user(user_id: str, db: Session = Depends(get_db)):
    return UserServiceDB(db).get_user_by_id(user_id)


@router.put(
    "/users/{user_id}",
    summary="Actualizar datos del usuario.",
    description="Aquí se le asigna el nombre al usuario",
    tags=["users"],
)
async def update_user(user_id: str, user: UserUpdate, db: Session = Depends(get_db)):
    return UserServiceDB(db).update_user(user_id, user)


@router.delete(
    "/users/{user_id}",
    summary="Borrar usuario",
    description="Borrar al usuario",
    tags=["users"],
)
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    return UserServiceDB(db).delete_user(user_id)


@router.post(
    "/users/{email}",
    summary="Reiniciar contraseña",
    description="Envia un a tu correo un link para cambiar la contraseña.",
    tags=["users"],
)
async def password_reset(email: str):
    return UserService().password_reset(email)
