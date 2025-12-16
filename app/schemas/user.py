from pydantic import BaseModel, EmailStr, validator
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @validator("password")
    def password_min_length(cls, v: str):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v




class UserLogin(BaseModel):
    email: EmailStr
    password: str



class UserResponse(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime



class UserInDB(BaseModel):
    email: EmailStr
    hashed_password: str
    created_at: datetime
