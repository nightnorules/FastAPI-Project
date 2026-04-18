from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.schemas.user import (
    UserCreate,
    UserResponse,
    LoginRequest,
    TokenResponse,
)
from backend.app.services.auth import AuthService
from backend.app.models.user import User
from backend.app.database.session import get_db
from backend.app.dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.register_user(user_data)


@router.post("/login", response_model=TokenResponse, summary="Login user")
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    user = await service.authenticate_user(login_data)
    access_token = service.create_access_token(user.id, user.email)
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )


@router.get("/me", response_model=UserResponse, summary="Get current user")
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)
