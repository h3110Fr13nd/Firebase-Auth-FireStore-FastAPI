from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from firebase_admin import auth
from utils import firestore_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")


async def get_current_user(
    token: str = Depends(oauth2_scheme), request: Request = None
):
    try:
        verified_token = auth.verify_id_token(token)
        auth_user = auth.get_user(verified_token["user_id"])
        uid = auth_user.uid
        user_doc_ref = firestore_db.collection("users").document(uid)
        auth_user.user_doc_ref = user_doc_ref
        request.state.auth_user = auth_user
        return auth_user
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail={"error": {"exception": type(e).__name__, "message": str(e)}},
        )
