import uvicorn
import firebase_admin
import pyrebase
import json

from firebase_admin import credentials, auth, firestore_async
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from models import SignUpSchema, LoginSchema

import requests





cred = credentials.Certificate("private_key.json")

firebase = firebase_admin.initialize_app(cred)



firestore_db = firestore_async.client()

firebase_config = json.load(open("firebase_config.json"))

app = FastAPI(
    title="Firebase Auth API",
    description="Firebase Auth API",
    docs_url="/",
)

allow_all = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=allow_all,
    allow_methods=allow_all,
    allow_headers=allow_all,
)


# @app.exception_handler(AssertionError)
# async def validation_exception_handler(request, exc):
#     return JSONResponse(
#         status_code=400,
#         content={"message": exc.args[0]},
#     )


# signup route
@app.post("/signup")
async def signup(user: SignUpSchema, ):
    username = user.username
    email = user.email
    password = user.password
    full_name = user.full_name
    if email is None or password is None or full_name is None:
        return HTTPException(
            detail={"message": "Error! Missing Email or Password or full_name"},
            status_code=400,
        )
    try:
        created_user = auth.create_user(email=email, password=password)
        created_at = created_user.user_metadata.creation_timestamp

        user_ref = firestore_db.collection('users').document(created_user.uid)
        await user_ref.set({
            'email': email,
            'username': username,
            'full_name': full_name,
            'created_at': created_at
        })
        
        return JSONResponse(
            content={"message": f"Successfully created user {created_user.uid}"},
            status_code=200,
        )
    except Exception as e:
        print(e)

        return HTTPException(detail={"message": "Error Creating User"}, status_code=400)


@app.post("/login")
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
    

        

# ping route
@app.post("/ping")
async def validate(request: Request):
    headers = request.headers
    jwt = headers.get("authorization")
    print(f"jwt:{jwt}")
    user = auth.verify_id_token(jwt)
    print(f"user:{user}")
    return user["uid"]


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
