import re
from pydantic import BaseModel, validator


class UserSchema(BaseModel):
    username: str
    email: str
    full_name: str
    created_at: str = None

    @validator("username")
    def username_alphanumeric(cls, v):
        assert v.isalnum(), "must be alphanumeric"
        assert len(v) >= 3, "must be 3 characters or more"
        assert len(v) <= 20, "must be 20 characters or less"
        return v

    @validator("full_name")
    def full_name_validator(cls, v):
        assert len(v) >= 3, "must be 3 characters or more"
        assert len(v) <= 50, "must be 50 characters or less"
        return v

    @validator("email")
    def email_validator(cls, v):
        regex = r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$"
        assert re.search(regex, v), "must be a valid email"
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@email.com",
                "full_name": "John Doe",
            }
        }
