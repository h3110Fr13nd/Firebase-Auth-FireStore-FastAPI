from fastapi import APIRouter, Request


from schemas.users import UserSchema
from schemas.auth import PasswordResetSchema
from fastapi.responses import JSONResponse
from utils import firestore_db, ExceptionResponse
from firebase_admin import auth
from utils import user_exists

router = APIRouter()


# Get User Profile
@router.get("/me")
async def get_user(request: Request = None):
    try:
        auth_user = request.state.auth_user
        user = await auth_user.user_doc_ref.get()
        
        return user.to_dict()
    except Exception as e:
        return ExceptionResponse(e)


# Update User Profile
@router.put("/me")
async def update_user(updated_user: UserSchema, request: Request = None):
    updated_email = updated_user.email
    updated_username = updated_user.username
    updated_fullname = updated_user.full_name
    if await user_exists(updated_username) :
        """If the user already exists, return a 400"""
        return ExceptionResponse(name="UserNameExists", message=f"User with {updated_username} already exists")
    try:
        auth_user = request.state.auth_user
        auth.update_user(
            auth_user.uid, email=updated_email, display_name=updated_fullname
        )
        user = await auth_user.user_doc_ref.get()
        user_dict = user.to_dict()
        user_dict["email"] = updated_email
        user_dict["username"] = updated_username
        user_dict["full_name"] = updated_fullname
        await auth_user.user_doc_ref.set(user_dict)
        return user_dict
    except Exception as e:
        return ExceptionResponse(e)


# Delete User Profile
@router.delete("/me")
async def delete_user(request: Request = None):
    try:
        auth_user = request.state.auth_user
        auth.delete_user(auth_user.uid)
        await auth_user.user_doc_ref.delete()
        return JSONResponse(
            status_code=200,
            content={"detail": {"message": "User deleted successfully"}},
        )
    except Exception as e:
        return ExceptionResponse(e)


@router.post("/me/password-reset")
async def reset_password(user: PasswordResetSchema, request: Request = None):
    new_password = user.new_password
    try:
        auth_user = request.state.auth_user
        auth.update_user(auth_user.uid, password=new_password)
        user = await auth_user.user_doc_ref.get()
        user_dict = user.to_dict()
        return user_dict
    except Exception as e:
        return ExceptionResponse(e)
