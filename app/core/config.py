import os
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


# Function to search for .env
def get_env_file():
    env = os.getenv("ENVIRONMENT", "development")
    if env == "production":
        return ".env.prod"
    return ".env.dev"


class Settings(BaseSettings):
    # App Info
    ENVIRONMENT: str
    DEBUG: bool
    APP_NAME: str

    # Auth/JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    # Admin seed
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    ADMIN_FULL_NAME: str
    ADMIN_EMAIL: str
    ADMIN_DISABLED: bool = False

    # Rate Limiting
    ENABLE_RATE_LIMITER: bool = False
    RATE_LIMIT_REQUESTS: int
    RATE_LIMIT_WINDOW: int

    # MySQL
    MYSQL_ROOT_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str

    # Database
    DATABASE_URL: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASS: str

    # Redis
    REDIS_LOCATION: str
    REDIS_PORT: int

    # CORS
    ALLOWED_ORIGINS: List[str]

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int
    RATE_LIMIT_WINDOW: int

    # Logs
    LOG_LEVEL: str

    model_config = SettingsConfigDict(
        env_file=get_env_file(), env_file_encoding="utf-8"
    )


settings = Settings()
