from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="UTF-8")

    app_name: str = "FastAPI Shop"
    debug_enabled: bool = Field(default=False)
    database_url: str = Field(..., description="Database URL")

    jwt_secret_key: str = Field(..., min_length=32, description="JWT secret key")
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24

    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    static_dir: str = "static"
    images_dir: str = "static/images"

    redis_url: str = "redis://redis:6379/0"

    celery_broker_url: str = "redis://redis:6379/1"
    celery_result_backend: str = "redis://redis:6379/2"

    @field_validator("jwt_secret_key")
    def validate_secret_key(cls, v):
        if "change-in-production" in v or v == "your-secret-key":
            raise ValueError("Must set a secure secret key")
        return v


settings = Settings()
