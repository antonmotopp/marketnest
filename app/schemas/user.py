from pydantic import BaseModel, EmailStr

class UserModel(BaseModel):
    username: str
    password: str

class User(BaseModel):
    username: str
    password: str
    email: EmailStr

class LoginRequest(UserModel):
    pass


class UserCreate(User):
    pass


class UserResponse(User):
    pass


    model_config = {"from_attributes": True}


