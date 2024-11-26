from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    """Schema base para información común de usuario."""

    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    username: str = Field(
        ..., min_length=3, max_length=50, description="Nombre de usuario"
    )
    first_name: str = Field(..., min_length=2, max_length=80, description="Nombre")
    first_last_name: str = Field(
        ..., min_length=2, max_length=50, description="Primer apellido"
    )
    second_last_name: str = Field(
        ..., min_length=2, max_length=50, description="Segundo apellido"
    )
    profile_picture_url: Optional[str] = Field(
        None, description="URL de la foto de perfil"
    )


class CreateUserSchema(UserBase):
    """Schema para crear un nuevo usuario."""

    password: str = Field(..., min_length=8, description="Contraseña del usuario")
    is_admin: bool = Field(
        default=False, description="Indica si el usuario es administrador"
    )


class ResponseUserSchema(UserBase):
    """Schema para la respuesta con información del usuario."""

    user_id: str = Field(..., description="ID único del usuario")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")
    is_active: bool = Field(..., description="Estado del usuario")
    email_verified: bool = Field(..., description="Estado de verificación del email")
    is_admin: bool = Field(..., description="Rol de administrador")

    model_config = ConfigDict(from_attributes=True)


class UpdateUserSchema(BaseModel):
    """Schema para actualizar información del usuario."""

    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    first_last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    second_last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    profile_picture_url: Optional[str] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(
        from_attributes=True,
        # json_schema_extra={
        #     "example": {
        #         "first_name": "John",
        #         "first_last_name": "Doe",
        #         "second_last_name": "Smith",
        #         "username": "johndoe",
        #         "is_active": True,
        #     }
        # },
    )


class LoginUserSchema(BaseModel):
    """Schema para el login de usuario."""

    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., min_length=8, description="Contraseña del usuario")


class LoginResponseSchema(BaseModel):
    """Schema para la respuesta del login."""

    email: EmailStr = Field(..., description="Email del usuario")
    token: str = Field(..., description="Token de acceso")
    refresh_token: str = Field(..., description="Token de actualización")

    model_config = ConfigDict(from_attributes=True)

