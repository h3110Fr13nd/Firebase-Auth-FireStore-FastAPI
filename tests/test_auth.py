import json
from fastapi.testclient import TestClient
from main import app
from unittest import TestCase
import firebase_admin
from firebase_admin import auth, firestore
import asyncio



class TestAuth(TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.test_user = None

    def tearDownClass(cls):
        # Delete test user from Firebase
        if cls.test_user == None:
            return
        uid = cls.test_user.uid
        auth.delete_user(cls.test_user.uid)

        # Delete test user from Firestore
        firestore_db = firestore.client()
        user_ref = firestore_db.collection("users").document(uid)
        user_ref.delete()

    
    
    def test_signup(self):
        # Test successful signup
        response = self.client.post(
            "/auth/signup",
            json={
                "username": "testuser",
                "email": "testuser@example.com",
                "password": "test@Password123",
                "full_name": "Test User"
            }
        )
        print(response.json())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["username"], "testuser")
        self.assertEqual(response.json()["email"], "testuser@example.com")
        self.assertEqual(response.json()["full_name"], "Test User")

        # Save test user for cleanup
        self.test_user = auth.get_user_by_email("testuser@example.com")
    
    def test_signup_existing_username_exception(self):
        # Test signup with existing username
        print("Testing signup with existing username")
        response = self.client.post(
            "/auth/signup",
            json={
                "username": "testuser",
                "email": "testuser@example.com",
                "password": "test@Password123",
                "full_name": "Test User"
            }
        )
        print(response.json())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"]["error"]["exception"], "UserNameExists")
        self.assertEqual(response.json()["detail"]["error"]["message"], "User with testuser already exists")


    def test_signup_existing_email_exception(self):

        # Test signup with existing email
        print("Testing signup with existing email")
        response = self.client.post(
            "/auth/signup",
            json={
                "username": "testuser2",
                "email": "testuser@example.com",
                "password": "test@Password123",
                "full_name": "Test User 2"
            }
        )
        print(response.json())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"]["error"]["exception"], "EmailExists")
        self.assertEqual(response.json()["detail"]["error"]["message"], "Email testuser@example.com already exists")

