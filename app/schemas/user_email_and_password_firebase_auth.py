from pydantic import BaseModel, EmailStr, Field


class UserResponse(BaseModel):
    uid: str
    email: EmailStr
    display_name: str | None = None
    email_verified: bool


class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    password: str = Field(..., min_length=6, description="Contraseña del usuario")


class UserNameUpdate(BaseModel):
    user_id: str = Field(
        ..., description="Id del usuario que se desea cambiar el nombre"
    )
    user_name: str = Field(..., description="Nuevo nombre del usuario")


class UserRecoveryPassword(BaseModel):
    email: EmailStr = Field(
        ..., description="Correo electronico para recupear contraseña."
    )
