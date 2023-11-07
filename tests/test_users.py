from fastapi.testclient import TestClient
from main import app
import requests
import asyncio
from firebase_admin import auth


client = TestClient(app)

def users_get():
    # Create test user
    user_create = client.post(
        "/auth/signup",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "test@Password123",
            "full_name": "Test User"
        }
    )
    assert user_create.status_code == 201

    # Get authentication token
    auth = client.post(
        "/auth/signin",
        json={
            "email": "testuser@example.com",
            "password": "test@Password123"
        }
    )
    assert auth.status_code == 200
    auth_token = auth.json()["access_token"]
    print("Auth token: ", auth_token)

    # Test authorized get request
    response = client.get("/users/me", headers={"Authorization": f"Bearer {auth_token}"})
    print(response.json())
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"
    assert response.json()["username"] == "testuser"
    assert response.json()["full_name"] == "Test User"

    # Test unauthorized get request
    response = client.get("/users/me", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401

def test_users_get():
    asyncio.run(users_get())


def users_put():
    auth = client.post(
        "/auth/signin",
        json={
            "email": "testuser@example.com",
            "password": "test@Password123"
        }
    )
    assert auth.status_code == 200
    auth_token = auth.json()["access_token"]
    print("Auth token: ", auth_token)
    # Test successful put request
    
    response = client.put("/users/me", json={
        "email":"testuser@example.com", 
        "username":"testuser",
        "full_name":"Updated User"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    print(response.json())


    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"
    assert response.json()["username"] == "testuser"
    assert response.json()["full_name"] == "Updated User"

    # Test unauthorized put request
    response = client.put("/users/me", json={
        "email":"testuser@example.com", 
        "username":"testuser",
        "full_name":"Updated User"
    }, headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401

def test_users_put():
    asyncio.run(users_put())

def users_reset_password():
    auth = client.post(
        "/auth/signin",
        json={
            "email": "testuser@example.com",
            "password": "test@Password123"
        }
    )
    assert auth.status_code == 200
    auth_token = auth.json()["access_token"]
    print("Auth token: ", auth_token)
    response = client.post("/users/me/password-reset", json={"new_password": "test@Password1234"}, 
                           headers={"Authorization": f"Bearer {auth_token}"})
    print(response.json())
    assert response.status_code == 200

    # Test unauthorized reset password request
    response = client.post("/users/me/password-reset", json={"new_password": "test@Password1234"},
                           headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401

def test_users_reset_password():
    asyncio.run(users_reset_password())

def users_delete():
    auth = client.post(
        "/auth/signin",
        json={
            "email": "testuser@example.com",
            "password": "test@Password1234"
        }
    )
    assert auth.status_code == 200
    auth_token = auth.json()["access_token"]
    print("Auth token: ", auth_token)
    # Test successful delete request
    response = client.delete("/users/me", headers={"Authorization": f"Bearer {auth_token}"})
    print(response.json())
    assert response.status_code == 200

    # Test unauthorized delete request
    response = client.delete("/users/me", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401


def test_users_delete():
    asyncio.run(users_delete())
    
