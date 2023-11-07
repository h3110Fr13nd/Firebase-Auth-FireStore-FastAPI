import uvicorn
from routers import auth, users
from dependencies import get_current_user
from fastapi import Depends
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Firebase Auth API",
    description="Firebase Auth API",
)

allow_all = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=allow_all,
    allow_methods=allow_all,
    allow_headers=allow_all,
)

app.include_router(
    router=auth.router,
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
),
app.include_router(
    router=users.router,
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
    dependencies=[
        Depends(get_current_user),
    ],
)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
