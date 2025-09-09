from pydantic import BaseModel, EmailStr

class UserModel(BaseModel):
    username: str

class LoginRequest(UserModel):
    password: str

class UserCreate(UserModel):
    email: EmailStr
    password: str

class UserResponse(UserModel):
    email: EmailStr


    model_config = {"from_attributes": True}

