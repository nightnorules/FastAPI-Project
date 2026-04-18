from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="UTF-8")

    app_name: str = "FastAPI Shop"
    debug: str | bool = True
    database_url: str = "postgresql+asyncpg://shop_user:shop_password@db:5432/shop_db"

    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24

    cors_origins: str = (
        "http://localhost:5173,"
        "http://localhost:3000,"
        "http://127.0.0.1:5173,"
        "http://127.0.0.1:3000"
    )

    static_dir: str = "static"
    images_dir: str = "static/images"

    redis_url: str = "redis://localhost:6379/0"

    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    smtp_server: str = "localhost"
    smtp_port: int = 587
    smtp_user: str = "noreply@shop.com"
    smtp_password: str = "your-smtp-password"
    smtp_from_email: str = "noreply@shop.com"

settings = Settings()
