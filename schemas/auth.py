from pydantic import BaseModel, validator
from .users import UserSchema
import re


class SignUpSchema(UserSchema):
    password: str

    @validator("password")
    def password_validator(cls, v):
        assert len(v) >= 8, "must be 8 characters or more"
        assert len(v) <= 20, "must be 20 characters or less"
        assert any(
            char.isupper() for char in v
        ), "must have at least one uppercase letter"
        assert any(
            char.islower() for char in v
        ), "must have at least one lowercase letter"
        assert any(char.isdigit() for char in v), "must have at least one digit"
        assert any(
            char in """ !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~""" for char in v
        ), """must have at least one special symbol from \n Each character as unique symbol : <begin list> !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~<end list>"""
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@email.com",
                "password": "john@123doe",
                "full_name": "John Doe",
            }
        }


class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "johndoe@email.com",
                "password": "john@123doe",
            }
        }


class PasswordResetSchema(BaseModel):
    new_password: str

    class Config:
        json_schema_extra = {
            "example": {
                "password": "john@123doe",
                "new_password": "john@123Doe",
            }
        }

    @validator("new_password")
    def password_validator(cls, v):
        assert len(v) >= 8, "must be 8 characters or more"
        assert len(v) <= 20, "must be 20 characters or less"
        assert any(
            char.isupper() for char in v
        ), "must have at least one uppercase letter"
        assert any(
            char.islower() for char in v
        ), "must have at least one lowercase letter"
        assert any(char.isdigit() for char in v), "must have at least one digit"
        assert any(
            char in """ !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~""" for char in v
        ), """must have at least one special symbol from \n Each character as unique symbol : <begin list> !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~<end list>"""
        return v
