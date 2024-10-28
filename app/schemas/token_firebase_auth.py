from pydantic import BaseModel, EmailStr, Field


class TokenRequest(BaseModel):
    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    password: str = Field(..., description="Contraseña del usuario")


class TokenVerify(BaseModel):
    token_id: str = Field(..., description="Token generado para validar")
