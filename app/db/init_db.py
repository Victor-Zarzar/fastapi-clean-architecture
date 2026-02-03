from sqlalchemy.orm import Session

from app.core.config import logger, settings
from app.services.user_service import ensure_admin
from app.utils.utils import get_password_hash


def seed_admin(db: Session) -> None:
    try:
        admin = ensure_admin(
            db,
            username=settings.ADMIN_USERNAME,
            password=get_password_hash(settings.ADMIN_PASSWORD),
            full_name=settings.ADMIN_FULL_NAME,
            email=settings.ADMIN_EMAIL,
            disabled=settings.ADMIN_DISABLED,
        )

        if admin:
            logger.info("Admin verified or successfully created.")
        else:
            logger.warning("No admin creation action was required.")

    except Exception as e:
        logger.error(f"Error when trying to create/verify admin: {e}")
        raise
