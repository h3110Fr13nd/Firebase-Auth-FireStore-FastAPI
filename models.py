from pydantic import BaseModel
from pydantic import validator
import re

class SignUpSchema(BaseModel):
    username: str
    email: str
    password: str
    full_name: str
    class Config:
        json_schema_extra = {
            "example": {
                "email": "johndoe@email.com",
                "password": "john@123doe",
                "full_name": "John Doe",
            }
        }

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        assert len(v) >= 3, 'must be 3 characters or more'
        assert len(v) <= 20, 'must be 20 characters or less'
        return v
    
    @validator('password')
    def password_validator(cls, v):
        assert len(v) >= 8, 'must be 8 characters or more'
        assert len(v) <= 20, 'must be 20 characters or less'
        assert any(char.isupper() for char in v), 'must have at least one uppercase letter'
        assert any(char.islower() for char in v), 'must have at least one lowercase letter'
        assert any(char.isdigit() for char in v), 'must have at least one digit'
        assert any(char in """ !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~""" for char in v), """must have at least one special symbol from \n Each character as unique symbol : <begin list> !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~<end list>"""
        return v
    
    @validator('full_name')
    def full_name_validator(cls, v):
        assert len(v) >= 3, 'must be 3 characters or more'
        assert len(v) <= 50, 'must be 50 characters or less'
        return v
    
    @validator('email')
    def email_validator(cls, v):
        # email regex
        regex = r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$"

        if(re.search(regex, v)):
            return v
        else:
            raise ValueError("Invalid Email")

    

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
    