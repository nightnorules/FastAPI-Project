from datetime import datetime
import re

from pydantic import BaseModel, ConfigDict, Field, field_validator

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class UserBase(BaseModel):
    email: str = Field(description="User email address")
    full_name: str | None = Field(None, max_length=255, description="User full name")

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not EMAIL_RE.match(normalized):
            raise ValueError("Invalid email address")
        return normalized


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=100, description="User password")


class UserResponse(UserBase):
    id: int = Field(description="User ID")
    is_active: bool = Field(description="Is user active")
    created_at: datetime = Field(description="User creation date")

    model_config = ConfigDict(from_attributes=True)



class LoginRequest(BaseModel):
    email: str = Field(description="User email")
    password: str = Field(min_length=8, description="User password")

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not EMAIL_RE.match(normalized):
            raise ValueError("Invalid email address")
        return normalized


class TokenResponse(BaseModel):
    access_token: str = Field(description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    user: UserResponse = Field(description="User information")


class TokenData(BaseModel):
    email: str | None = None
    user_id: int | None = None
