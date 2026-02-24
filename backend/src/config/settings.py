"""
Application configuration settings.
Environment variables are loaded from .env file.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # Application
    APP_NAME: str = "InnovatEPAM Portal"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Password hashing
    BCRYPT_ROUNDS: int = 12
    
    # Database
    DATABASE_URL: str
    DATABASE_ECHO: bool = False
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    
    # File uploads
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB in bytes
    UPLOAD_DIR: str = "uploads"
    ALLOWED_EXTENSIONS: list[str] = [
        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
    ]
    ALLOWED_MIME_TYPES: list[str] = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "image/jpeg",
        "image/png",
        "image/gif",
    ]
    
    # Rate limiting
    RATE_LIMIT_REGISTRATION_PER_HOUR: int = 3
    RATE_LIMIT_LOGIN_PER_15MIN: int = 5
    RATE_LIMIT_REFRESH_PER_HOUR: int = 10

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
