from sqlalchemy.orm import Session
from app.crud.crud_user import UserDB
from firebase_admin import auth
from fastapi import HTTPException, status
from app.db.models.users import User
from app.schemas.user import (
    CreateUserSchema,
    LoginResponseSchema,
    ResponseUserSchema,
    UpdateUserSchema,
    LoginUserSchema,
)
import requests
import os


class UserServiceDB:
    def __init__(self, db: Session):
        self.user_db = UserDB(db)
        self.db = db

    def create_user(self, user: CreateUserSchema):
        try:
            existing_user = (
                self.db.query(User).filter(User.username == user.username).first()
            )
            if existing_user:
                raise HTTPException(
                    status_code=400, detail="Username already exists in database"
                )

            try:
                firebase_user = auth.create_user(
                    email=user.email, password=user.password
                )
                firebase_uid = firebase_user.uid
            except auth.EmailAlreadyExistsError:
                firebase_user = auth.get_user_by_email(user.email)
                firebase_uid = firebase_user.uid

                existing_firebase_user = (
                    self.db.query(User).filter(User.user_id == firebase_uid).first()
                )
                if existing_firebase_user:
                    raise HTTPException(
                        status_code=400,
                        detail="User already exists in both Firebase and MySQL",
                    )

            return self.user_db.create_user(firebase_uid, user)
        except HTTPException as e:
            raise HTTPException(status_code=400, detail=f"Error users: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_user_current_data(self, token: dict) -> ResponseUserSchema:
        try:
            user_id = auth.get_user(token["uid"])
            user = self.user_db.get_user_by_id(user_id.uid)
            return ResponseUserSchema(
                user_id=user_id.uid,
                email=user.email,  # type: ignore
                username=user.username,  # type: ignore
                first_name=user.first_name,  # type: ignore
                first_last_name=user.first_last_name,  # type: ignore
                second_last_name=user.second_last_name,  # type: ignore
                profile_picture_url=user.profile_picture_url,  # type: ignore
                created_at=user.created_at,  # type: ignore
                updated_at=user.updated_at,  # type: ignore
                is_active=user.is_active,  # type: ignore
                email_verified=user_id.email_verified,
                is_admin=user.is_admin,  # type: ignore
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener información del usuario: {str(e)}",
            )

    def update_user(self, user: UpdateUserSchema, token: dict):
        return self.user_db.update_user(user, token)

    def delete_user(self, token: dict):
        try:
            auth.delete_user(token["uid"])
            return self.user_db.delete_user(token["uid"])
        except auth.UidAlreadyExistsError:
            raise HTTPException(status_code=404, detail="User not found")


class UserService:
    def __init__(self) -> None:
        pass

    def password_reset(self, email: str):
        payload = {"requestType": "PASSWORD_RESET", "email": email}
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={os.getenv('FIREBASE_API_KEY')}"

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return {"message": "Password reset email sent"}
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=str(e))

    def refresh_token(self, refresh_token: str):
        url = f"https://securetoken.googleapis.com/v1/token?key={os.getenv('FIREBASE_API_KEY')}"
        payload = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        try:
            response = requests.post(url, json=payload)

            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Error al refrescar el token",
                )

            return response.json()

        except requests.exceptions.RequestException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error en la conexión con Firebase",
            )

    def login(self, user: LoginUserSchema):
        try:
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={os.getenv('FIREBASE_API_KEY')}"

            payload = {
                "email": user.email,
                "password": user.password,
                "returnSecureToken": True,
            }

            response = requests.post(url, json=payload)

            if response.status_code != 200:
                error_data = response.json()
                error_message = error_data.get("error", {}).get(
                    "message", "Error en el login"
                )

                error_mapping = {
                    "EMAIL_NOT_FOUND": "Email no encontrado",
                    "INVALID_PASSWORD": "Contraseña incorrecta",
                    "USER_DISABLED": "Usuario deshabilitado",
                }

                detail = error_mapping.get(error_message, error_message)

                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail=detail
                )

            return LoginResponseSchema(
                email=response.json()["email"],
                token=response.json()["idToken"],
                refresh_token=response.json()["refreshToken"],
            )

        except requests.exceptions.RequestException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error en la conexión con Firebase",
            )

    def logout(self, token: dict):
        try:
            auth.revoke_refresh_tokens(token["uid"])
            return {"message": "Sesión cerrada exitosamente"}
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al cerrar sesión",
            )

    def verify_email(self, token: str):
        firebase_api_key = os.getenv("FIREBASE_API_KEY")
        if not firebase_api_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="La API key de Firebase no está configurada correctamente.",
            )

        url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={os.getenv('FIREBASE_API_KEY')}"
        headers = {"Content-Type": "application/json"}
        payload = {"requestType": "VERIFY_EMAIL", "idToken": token}

        try:
            requests.post(url, headers=headers, json=payload)
            return {"message": "The verification email was sent to your email"}
        except requests.exceptions.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Error al enviar el correo de verificación: {str(e)}",
            )
        except requests.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error en la conexión con Firebase: {str(e)}",
            )
