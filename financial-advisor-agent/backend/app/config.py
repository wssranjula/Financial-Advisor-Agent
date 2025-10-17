"""
Application configuration using Pydantic Settings
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    APP_NAME: str = "Financial Advisor AI Agent"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Google OAuth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    # HubSpot OAuth
    HUBSPOT_CLIENT_ID: str
    HUBSPOT_CLIENT_SECRET: str
    HUBSPOT_REDIRECT_URI: str

    # API Keys
    ANTHROPIC_API_KEY: str
    OPENAI_API_KEY: str

    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"

    # Security
    ENCRYPTION_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


# Create settings instance
settings = Settings()
