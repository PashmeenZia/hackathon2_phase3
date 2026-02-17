from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Dict, Any
from pydantic import BaseModel
from src.models.database import get_db
from src.models.user import User
from src.core.security import verify_password, create_access_token, get_password_hash


router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: Dict[str, Any]


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str = None


class RegisterResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: Dict[str, Any]


@router.post("/auth/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return access token
    """
    # Find user by email
    user = db.query(User).filter(User.email == login_data.email).first()

    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is deactivated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    token_data = {
        "sub": user.id,
        "email": user.email,
        "user_id": user.id
    }
    access_token = create_access_token(data=token_data)

    # Calculate expiration time in seconds
    expires_in = 30 * 60  # 30 minutes in seconds

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=expires_in,
        user={
            "id": user.id,
            "email": user.email
        }
    )


@router.post("/auth/register", response_model=RegisterResponse, status_code=status.HTTP_200_OK)
async def register(
    register_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == register_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    user = User(
        email=register_data.email,
        password_hash=get_password_hash(register_data.password),
        is_active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # Create access token for the new user
    token_data = {
        "sub": user.id,
        "email": user.email,
        "user_id": user.id
    }
    access_token = create_access_token(data=token_data)
    expires_in = 30 * 60  # 30 minutes in seconds

    return RegisterResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=expires_in,
        user={
            "id": user.id,
            "email": user.email
        }
    )




@router.post("/auth/logout")
async def logout():
    """
    Logout endpoint (for future token blacklisting)
    """
    # In a stateless JWT system, logout is typically handled on the client side
    # However, we might want to implement token blacklisting in the future
    return {"message": "Logged out successfully"}