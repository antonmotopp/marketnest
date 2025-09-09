from pydantic import BaseModel

class UserModel(BaseModel):
    username: str

class LoginRequest(UserModel):
    password: str

class UserCreate(UserModel):
    email: str
    password: str

class UserResponse(UserModel):
    email: str


    model_config = {"from_attributes": True}

