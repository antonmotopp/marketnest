from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# API'den dönecek response (şifre yok)
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True