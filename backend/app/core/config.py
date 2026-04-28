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

    @property
    def cors_origins_list(self) -> list:
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()
