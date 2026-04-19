import logging
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import settings
from backend.app.models.user import User
from backend.app.repositories.user import UserRepository
from backend.app.schemas.user import (
    LoginRequest,
    TokenData,
    UserCreate,
    UserResponse,
)

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(
        user_id: int, email: str, expires_delta: timedelta | None = None
    ) -> str:
        if expires_delta is None:
            expires_delta = timedelta(hours=settings.jwt_expiration_hours)

        expire = datetime.now(timezone.utc) + expires_delta
        to_encode = {
            "sub": email,
            "user_id": user_id,
            "exp": expire,
            "iat": datetime.now(timezone.utc),
        }

        encoded_jwt = jwt.encode(
            to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
        )
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> TokenData:

        try:
            payload = jwt.decode(
                token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
            )
            email: str = payload.get("sub")
            user_id: int = payload.get("user_id")

            if email is None or user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
                )
            return TokenData(email=email, user_id=user_id)
        except JWTError as e:
            logger.warning(f"Invalid token: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

    async def register_user(self, user_data: UserCreate) -> UserResponse:
        existing_user = await self.repository.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
            )

        hashed_password = self.hash_password(user_data.password)
        try:
            user = await self.repository.create(user_data, hashed_password)
            return UserResponse.model_validate(user)
        except IntegrityError:
            logger.warning(f"Duplicate email in registration: {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
            )

    async def authenticate_user(self, login_data: LoginRequest) -> User:
        user = await self.repository.get_by_email(login_data.email)
        if not user or not self.verify_password(
            login_data.password, user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive"
            )

        return user

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return UserResponse.model_validate(user)
