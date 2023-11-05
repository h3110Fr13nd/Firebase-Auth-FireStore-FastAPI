from fastapi import APIRouter, HTTPException

router = APIRouter()

# Get User Profile
@router.get("/me")
def get_user():
    return {"message": "Hello World"}

# Update User Profile
@router.put("/me")
def update_user():
    return {"message": "Hello World"}

# Delete User Profile
@router.delete("/me")
def delete_user():
    return {"message": "Hello World"}
