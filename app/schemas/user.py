from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: str

class LoginRequest(UserBase):

    password: str

class UserCreate(UserBase):

    password: str

class UserResponse(UserBase):
    id: int


    model_config = {
        "from_attributes": True
    }
