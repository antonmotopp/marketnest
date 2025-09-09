from fastapi import APIRouter, HTTPException, Depends, status
from app.core.security import verify_password, create_access_token, get_current_user
from app.models.user import User
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.schemas.user import LoginRequest, UserCreate, UserResponse

router = APIRouter()

@router.post(
    '/login',
    summary="User Login",
    description="Endpoint for user authentication. Users can log in using their credentials."
)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()

    if not user or not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=401,
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

@router.post(
    "/register",
    summary="User Registration",
    description="*Endpoint for a new user registration with email/username validation and password hashing.*",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # *Check if username or email exists*
    existing_user = db.query(DBUser).filter(
        (DBUser.username == user.username) | (DBUser.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="*Username or email already exists*"
        )

    new_user = DBUser(username=user.username, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
    "username": new_user.username,
    "email": new_user.email
    }

