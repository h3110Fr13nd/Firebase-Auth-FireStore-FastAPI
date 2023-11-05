import firebase_admin
from firebase_admin import credentials, firestore_async
import json

cred = credentials.Certificate("private_key.json")
firebase = firebase_admin.initialize_app(cred)
firestore_db = firestore_async.client(app=firebase)
firebase_config = json.load(open("firebase_config.json"))


