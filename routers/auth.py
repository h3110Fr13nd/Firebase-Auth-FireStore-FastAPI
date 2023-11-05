from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from schemas.auth import SignUpSchema, LoginSchema
import requests
from firebase_admin import credentials, auth, firestore_async
from utils import firestore_db

router = APIRouter()

@router.post("/signup")
async def signup(
    user: SignUpSchema,
):
    username = user.username
    email = user.email
    password = user.password
    full_name = user.full_name
    # Check firestore if username exists
    username_ref = (
        firestore_db.collection("users")
        .where(filter=firestore_async.firestore.FieldFilter("username", "==", username))
        .limit(1)
        .stream()
    )
    async for doc in username_ref:
        if doc.exists:
            return JSONResponse(
                content={"message": f"Username {username} already exists"},
                status_code=400,
            )
    try:
        created_user = auth.create_user(email=email, password=password)
        created_at = created_user.user_metadata.creation_timestamp

        user_ref = firestore_db.collection("users").document(created_user.uid)
        await user_ref.set(
            {
                "email": email,
                "username": username,
                "full_name": full_name,
                "created_at": created_at,
            }
        )

        return JSONResponse(
            content={"message": f"Successfully created user {created_user.uid}"},
            status_code=200,
        )
    except Exception as e:
        print(e)
        return HTTPException(detail={"message": str(e)}, status_code=400)


@router.post("/login")
async def loginfirebase(user: LoginSchema):
    email = user.email
    password = user.password
    try:
        signin_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_config['apiKey']}"
        payload = {"email": email, "password": password, "returnSecureToken": True}
        headers = {"Content-Type": "application/json"}
        response = requests.post(signin_url, headers=headers, json=payload)
        print(response.json())

        return JSONResponse(content=response.json(), status_code=200)
    except:
        return HTTPException(
            detail={"message": "There was an error logging in"}, status_code=400
        )
