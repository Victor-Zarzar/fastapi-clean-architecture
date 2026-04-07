import os

from pydantic_settings import BaseSettings, SettingsConfigDict


def get_env_file():
    env = os.getenv("ENVIRONMENT", "development")
    if env == "production":
        return ".env.prod"
    return ".env.dev"


class Settings(BaseSettings):
    ENVIRONMENT: str
    DEBUG: bool
    APP_NAME: str

    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    ADMIN_FULL_NAME: str
    ADMIN_EMAIL: str
    ADMIN_DISABLED: bool = False

    ENABLE_RATE_LIMITER: bool = False
    RATE_LIMIT_REQUESTS: int
    RATE_LIMIT_WINDOW: int

    MYSQL_ROOT_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str

    DATABASE_URL: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASS: str

    REDIS_LOCATION: str
    REDIS_PORT: int

    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_TOPIC: str
    KAFKA_CONSUMER_GROUP: str

    ALLOWED_ORIGINS: list[str]

    LOG_LEVEL: str

    LOKI_HTTP_PORT: int | None = None
    LOKI_GRPC_PORT: int | None = None
    LOKI_RETENTION_PERIOD: str | None = None
    LOKI_DATA_PATH: str | None = None

    PROMTAIL_HTTP_PORT: int | None = None
    PROMTAIL_POSITIONS_FILE: str | None = None
    LOKI_URL: str | None = None

    GRAFANA_PORT: int | None = None
    GRAFANA_ADMIN_USER: str | None = None
    GRAFANA_ADMIN_PASSWORD: str | None = None
    GRAFANA_DOMAIN: str | None = None
    GRAFANA_ROOT_URL: str | None = None

    NGINX_LOG_PATH: str | None = None

    model_config = SettingsConfigDict(
        env_file=get_env_file(), env_file_encoding="utf-8"
    )


settings = Settings()
