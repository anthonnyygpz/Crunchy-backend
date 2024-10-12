import os
import requests
from fastapi import APIRouter, HTTPException
from fastapi.security import HTTPBasic
from firebase_admin import auth

from app.schemas.firebaseAuth import (
    CreateUser,
    UserResponse,
    UserRegister,
)

router = APIRouter()
security = HTTPBasic()


@router.post("/register_user/{user_name}")
def create_user(user: CreateUser):
    try:
        user_record = auth.create_user(email=user.email, password=user.password)
        return {"message": "User created successfully!", "uid": user_record}
    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login_user/")
def login_user(user: UserRegister):
    try:
        api_key = os.getenv("FIREBASE_API_KEY")
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
        payload = {
            "email": user.email,
            "password": user.password,
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
    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/get_user/{uid}", response_model=UserResponse)
async def get_user(uid: str):
    try:
        user = auth.get_user(uid)
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


@router.post("/add_name/{uid}/{user_name}")
async def add_name(uid: str, user_name: str):
    try:
        user = auth.update_user(uid, display_name=user_name)
        return user
    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/disabled_user/{uid}")
def delete_user(uid: str):
    try:
        auth.update_user(uid, disabled=True)
        return {"message": "User deleted successfully!"}
    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
