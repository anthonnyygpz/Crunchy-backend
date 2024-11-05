from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_db
from sqlalchemy.orm import Session


from app.schemas.user import UserResponse, UserCreate
from app.db.models.user import User
from app.services.user import UserService

router = APIRouter()


@router.post(
    "/users/",
    response_model=UserResponse,
    summary="Crear usuarios",
    description="Registrar usuarios con autenticación",
    tags=["users"],
)
async def create_user(user: UserCreate, password: str, db: Session = Depends(get_db)):
    return UserService(db).create_user(user, password)


@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Obtener los datos del usuario.",
    description="Obtiene todo datos del usuario.",
    tags=["users"],
)
async def read_user(user_id: str, db: Session = Depends(get_db)):
    return UserService(db).get_user_by_id(user_id)


@router.put(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Actualizar datos del usuario.",
    description="Aquí se le asigna el nombre al usuario",
    tags=["users"],
)
async def update_user(user_id: str, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Task not found")

    for var, value in vars(user).items():
        setattr(db_user, var, value)

    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete(
    "/users/{user_id}",
    summary="Borrar usuario",
    description="Borrar al usuario",
    tags=["users"],
)
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_user)
    db.commit()
    return {"message": "Task deleted successfully"}


# @router.post(
#     "/users/{email_reset}",
#     response_model=dict,
#     summary="reinicio de contraseña.",
#     description="Se envia a tu correo electronico una url para restablecer la contraseña.",
#     tags=["users"],
# )
# async def send_password_reset(
#     email_reset: EmailStr = Path(
#         title="Correo electronico.",
#         description="Aqui se coloca el correo que se le enviara la url del restablecimiento de contraseña.",
#     ),
# ):
#     url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
#     data = {"requestType": "PASSWORD_RESET", "email": email_reset}
#     headers = {"Content-Type": "application/json"}
#     try:
#         response = requests.post(
#             url,
#             headers=headers,
#             json=data,
#             params={"key": os.getenv("FIREBASE_API_KEY")},
#         )
#         response.raise_for_status()
#         return {"message": "A password reset link has been sent to your email"}
#     except requests.exceptions.RequestException as e:
#         raise HTTPException(
#             status_code=500, detail=f"Error al enviar el correo: {str(e)}"
#         )
