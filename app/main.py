import logging

from fastapi import FastAPI

from app.core.config import settings
from app.core.limiter import setup_rate_limiter
from app.core.logger import logger
from app.middlewares.cors_middleware import add_cors
from app.services.redis_service import RedisManager
from app.views import admin, auth, costs, health, users

redis = RedisManager()


app = FastAPI(
    title=settings.APP_NAME,
    description="API Cost Map Brazilian",
    version="1.0.0",
    debug=settings.DEBUG,
)

add_cors(app)

logger.info("Logger loaded successfully!")
logging.getLogger("slowapi").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

setup_rate_limiter(app, enabled=settings.ENABLE_RATE_LIMITER)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(users.router, prefix="/api/v1", tags=["Users"])
app.include_router(costs.router, prefix="/api/v1", tags=["Costs"])
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
