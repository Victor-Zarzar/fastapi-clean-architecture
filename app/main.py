import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.routes import routers as v1_routers
from app.core.config import settings
from app.core.limiter import setup_rate_limiter
from app.core.logger import logger
from app.db.seed import run_dev_seed
from app.helpers.producer import producer
from app.helpers.redis import RedisManager
from app.middlewares.cors_middleware import add_cors

redis = RedisManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        run_dev_seed()
    except Exception as error:
        logger.warning(f"Seed startup failed: {error}")

    try:
        await producer.start()
        logger.info("Kafka producer started successfully.")
    except Exception as error:
        logger.warning(f"Kafka startup failed: {error}")

    yield

    try:
        await producer.stop()
    except Exception as error:
        logger.warning(f"Kafka producer stop failed: {error}")


def create_app() -> FastAPI:
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

    app.include_router(v1_routers, prefix=settings.API_V1_STR)

    return app


app = create_app()
