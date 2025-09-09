from fastapi import APIRouter, HTTPException, Depends, status
from app.core.security import verify_password, create_access_token, get_current_user
from app.models.user import User
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter()

@router.post(
    '/login',
    response_model=TokenResponse,
    summary="User Login",
    description="Endpoint for user authentication. Users can log in using their credentials."
)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()

    if not user or not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    access_token = create_access_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }

@router.post(
    '/logout',
    summary="User Logout",
    description="Endpoint for user logout. This will invalidate the user's session."
)
async def logout(current_user: User = Depends(get_current_user)):
    return {
        'message': f'User {current_user.username} successfully logged out',
        'status': 'success'
    }