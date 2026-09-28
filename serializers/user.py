# serializers/user.py

from pydantic import BaseModel

class UserRegistrationSchema(BaseModel):
    username: str  # User's unique name
    email: str  # User's email address
    password: str  # Plain text password for user registration (will be hashed before saving)

# Schema for returning user data (without exposing the password)
class UserSchema(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True


class UserTokenSchema(BaseModel):
    token: str  # JWT token generated upon successful login
    message: str  # Success message

    class Config:
        orm_mode = True

# Schemas for incoming data
class UserResponseSchema(BaseModel):
    username: str
    email: str

# New schema for user login (captures username and password during login)
class UserLoginSchema(BaseModel):
    username: str  # Username provided by the user during login
    password: str  # Plain text password