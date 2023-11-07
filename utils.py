import firebase_admin
from firebase_admin import credentials, firestore_async, auth
from firebase_admin.firestore_async import firestore
import json
from fastapi.responses import JSONResponse

cred = credentials.Certificate("private_key.json")
firebase = firebase_admin.initialize_app(cred)
firestore_db = firestore_async.client(app=firebase)
firebase_config = json.load(open("firebase_config.json"))


class ExceptionResponse(JSONResponse):
    def __init__(self, e=None, name=None, message=None, status_code=400):
        super().__init__(
            status_code=status_code,
            content={
                "detail": {
                    "error": {
                        "exception": name or type(e).__name__,
                        "message": message or str(e),
                    }
                }
            },
        )


async def user_exists(username):
    count_obj_ref =  (firestore_db.collection("users")
        .where(filter=firestore.FieldFilter("username", "==", username))
        .count())
    print(count_obj_ref)
    count_obj = await count_obj_ref.get()
    print(count_obj)
    count = count_obj[0][0].value
    print(count)
    return count > 0


async def create_user(email, password, username, full_name):
    # Create the user in Firebase
    created_user = auth.create_user(
        email=email, password=password, display_name=full_name
    )
    created_at = created_user.user_metadata.creation_timestamp

    # Create the user details in Firestore
    user_ref = firestore_db.collection("users").document(created_user.uid)
    user_set = await user_ref.set(
        {
            "email": email,
            "username": username,
            "full_name": full_name,
            "created_at": created_at,
        }
    )
    
    

    return await user_ref.get()
