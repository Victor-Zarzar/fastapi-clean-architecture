from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logger import logger
from app.services.user_service import UserService


def create_default(db: Session) -> None:
    try:
        service = UserService(db)
        admin = service.ensure_admin(
            username=settings.ADMIN_USERNAME,
            password=settings.ADMIN_PASSWORD,
            full_name=settings.ADMIN_FULL_NAME,
            email=settings.ADMIN_EMAIL,
            disabled=settings.ADMIN_DISABLED,
            email_verified=True,
        )
        if admin:
            logger.info("Admin verified or successfully created.")
        else:
            logger.warning("No admin creation action was required.")
    except Exception as e:
        logger.error(f"Error when trying to create/verify admin: {e}")
        raise
