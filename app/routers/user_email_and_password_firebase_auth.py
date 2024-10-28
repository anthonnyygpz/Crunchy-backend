from fastapi import APIRouter, HTTPException, Path
from firebase_admin import auth
from pydantic import EmailStr
from dotenv import load_dotenv
import requests
import os


from app.schemas.user_email_and_password_firebase_auth import (
    UserResponse,
    UserCreate,
    UserNameUpdate,
)

router = APIRouter()

load_dotenv()


@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Listar datos del usuario",
    description="Lista todo los datos del usuario como id, correo, nombre, etc",
    tags=["users"],
)
async def get_user(user_id: str):
    try:
        user = auth.get_user(user_id)
        return UserResponse(
            uid=user.uid,
            email=user.email,
            display_name=user.display_name,
            email_verified=user.email_verified,
        )
    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/users/",
    response_model=dict,
    summary="Crear usuarios",
    description="Registrar usuarios con autenticación",
    tags=["users"],
)
async def create_user(user_data: UserCreate):
    try:
        auth.create_user(email=user_data.email, password=user_data.password)
        return {"message": "User created successfully!"}
    except auth.EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Email already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/users/{user_id}",
    response_model=dict,
    summary="Desactivar usuario",
    description="Desactiva al usuario",
    tags=["users"],
)
async def update_user(
    user_id: str = Path(
        title="Id del usuario.",
        description="Aqui se coloca el id del usuario que se desea 'borrar'",
    ),
):
    try:
        auth.update_user(user_id, disabled=True)
        return {"message": "User deleted successfully!"}
    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/users/",
    summary="Actualizar nombre",
    description="Aquí se le asigna el nombre al usuario",
    tags=["users"],
)
async def update_name(user_data: UserNameUpdate):
    try:
        user = auth.update_user(user_data.user_id, display_name=user_data.user_name)
        return {
            "message": "Username updated successfully",
            "user": user["display_name"],
        }
    except auth.UserNotFoundError:
        raise HTTPException(status_code=400, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post(
    "/users/{email_reset}",
    response_model=dict,
    summary="reinicio de contraseña.",
    description="Se envia a tu correo electronico una url para restablecer la contraseña.",
    tags=["users"],
)
async def send_password_reset(
    email_reset: EmailStr = Path(
        title="Correo electronico.",
        description="Aqui se coloca el correo que se le enviara la url del restablecimiento de contraseña.",
    ),
):
    url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
    data = {"requestType": "PASSWORD_RESET", "email": email_reset}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            params={"key": os.getenv("FIREBASE_API_KEY")},
        )
        response.raise_for_status()
        return {"message": "A password reset link has been sent to your email"}
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500, detail=f"Error al enviar el correo: {str(e)}"
        )
