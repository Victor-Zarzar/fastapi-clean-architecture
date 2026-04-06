from sqlmodel import Session

from app.core.config import settings
from app.core.logger import logger
from app.db.create_default import create_default
from app.db.database import engine


def run_dev_seed() -> None:
    if not settings.DEBUG:
        logger.info("Skipping seed because application is not in DEBUG mode.")
        return

    try:
        with Session(engine) as db:
            create_default(db)
        logger.info("Development seed executed successfully.")
    except Exception as error:
        logger.error(f"Development seed failed: {error}")
        raise
