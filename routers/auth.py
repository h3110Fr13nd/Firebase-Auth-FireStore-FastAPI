from fastapi import APIRouter
from schemas.auth import SignUpSchema, LoginSchema
import requests

from utils import (
    user_exists,
    create_user,
    firebase_config,
    ExceptionResponse,
)

router = APIRouter()


# Create a new user
@router.post("/signup", status_code=201)
async def signup(user: SignUpSchema):
    username = user.username
    email = user.email
    password = user.password
    full_name = user.full_name

    if await user_exists(username):
        """If the user already exists, return a 400"""
        return ExceptionResponse(name="UserNameExists", message=f"User with {username} already exists")
    try:
        created_user = (await create_user(email, password, username, full_name))
        return created_user.to_dict()
    except Exception as e:
        # If there's an error, return a 400 with the error message
        return ExceptionResponse(e)


@router.post("/signin")
async def signin(user: LoginSchema):
    email = user.email
    password = user.password
    
    try:
        signin_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_config['apiKey']}"
        payload = {"email": email, "password": password, "returnSecureToken": True}
        headers = {"Content-Type": "application/json"}
        response = requests.post(signin_url, headers=headers, json=payload)
        json_response = response.json()
        if response.status_code != 200:
            return ExceptionResponse(name=json_response["error"]["message"], message="Password Entered is InValid")
        
        return {
            "user_id": json_response["localId"],
            "email": json_response["email"],
            "full_name": json_response["displayName"],
            "access_token": json_response["idToken"],
            "token_type": "bearer",
            "expires_in": int(json_response["expiresIn"]),
            "refresh_token": json_response["refreshToken"],
        }
    except Exception as e:
        return ExceptionResponse(e)
