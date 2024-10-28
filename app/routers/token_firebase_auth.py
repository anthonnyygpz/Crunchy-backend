from fastapi import APIRouter, HTTPException
from firebase_admin import auth
import requests
import os

from app.schemas.token_firebase_auth import TokenRequest, TokenVerify

router = APIRouter()


@router.post(
    "/generate-tokens/",
    response_model=dict,
    summary="Generador de tokens",
    description="Se genera el token del usuario",
    tags=["verify"],
)
async def generate_token(token_data: TokenRequest):
    try:
        api_key = os.getenv("FIREBASE_API_KEY")
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
        payload = {
            "email": token_data.email,
            "password": token_data.password,
            "returnSecureToken": True,
        }

        response = requests.post(url, json=payload)
        response_data = response.json()

        if "error" in response_data:
            raise HTTPException(
                status_code=400, detail=response_data["error"]["message"]
            )

        id_token = response_data["idToken"]
        return {"message": "User logged in successfully!", "id_token": id_token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/verify-tokens/",
    response_model=dict,
    summary="Verificar token",
    description="Verifica el token del usuario.",
    tags=["verify"],
)
async def verify_token(token_data: TokenVerify):
    try:
        decoded_token = auth.verify_id_token(token_data.token_id)
        uid = decoded_token["uid"]

        user = auth.get_user(uid)

        if not user.email_verified:
            link = auth.generate_email_verification_link(user.email)
            return {"message": link}

        return {"message": "User logged in successfully!"}
    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
