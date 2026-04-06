import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.limiter import setup_rate_limiter
from app.core.logger import logger
from app.db.seed import run_dev_seed
from app.helpers.producer import producer
from app.helpers.redis import RedisManager
from app.middlewares.cors_middleware import add_cors
from app.services.consumer_service import consumer
from app.views import admin, auth, costs, health, kafka, users

redis = RedisManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        run_dev_seed()
    except Exception as error:
        logger.warning(f"Seed startup failed: {error}")

    try:
        await producer.start()
        await consumer.start()
        logger.info("Kafka producer and consumer started successfully.")
    except Exception as error:
        logger.warning(f"Kafka startup failed: {error}")

    try:
        yield
    finally:
        try:
            await consumer.stop()
        except Exception as error:
            logger.warning(f"Kafka consumer stop failed: {error}")

        try:
            await producer.stop()
        except Exception as error:
            logger.warning(f"Kafka producer stop failed: {error}")


app = FastAPI(
    title=settings.APP_NAME,
    description="API Cost Map Brazilian",
    version="1.0.0",
    debug=settings.DEBUG,
    lifespan=lifespan,
)

add_cors(app)

logger.info("Logger loaded successfully!")
logging.getLogger("slowapi").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("aiokafka").setLevel(logging.WARNING)

setup_rate_limiter(app, enabled=settings.ENABLE_RATE_LIMITER)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(users.router, prefix="/api/v1", tags=["Users"])
app.include_router(costs.router, prefix="/api/v1", tags=["Costs"])
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(kafka.router, prefix="/api/v1/kafka", tags=["Kafka"])
