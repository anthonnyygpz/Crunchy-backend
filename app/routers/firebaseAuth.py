import os
from typing import Optional
import requests
from fastapi import APIRouter, HTTPException, Query
from fastapi.security import HTTPBasic
from firebase_admin import auth, credentials, initialize_app

from app.schemas.firebaseAuth import (
    CreateUser,
    UserResponse,
    UserList,
    UserRegister,
)

router = APIRouter()
security = HTTPBasic()


cred = credentials.Certificate("service-firebase.json")
initialize_app(cred)


@router.post("/register_user/")
def create_user(user: CreateUser):
    try:
        user_record = auth.create_user(email=user.email, password=user.password)
        return {"message": "User created successfully!", "uid": user_record}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create user: {str(e)}")


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
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to login user: {str(e)}")


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


@router.get("/list_users", response_model=UserList)
async def list_users(
    max_results: int = Query(1000, le=1000), page_token: Optional[str] = None
):
    try:
        page = auth.list_users(max_results=max_results, page_token=page_token)
        users = [
            UserResponse(
                uid=user.uid,
                email=user.email,
                display_name=user.display_name,
                email_verified=user.email_verified,
            )
            for user in page.users
        ]
        return UserList(users=users, next_page_token=page.next_page_token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list users: {str(e)}")


@router.put("/disabled_user/{uid}")
def delete_user(uid: str):
    try:
        auth.update_user(uid, disabled=True)
        return {"message": "User deleted successfully!"}
    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
