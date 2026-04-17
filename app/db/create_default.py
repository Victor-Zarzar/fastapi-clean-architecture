from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logger import logger
from app.repository.user import UserRepository
from app.services.two_factor_service import TwoFactorService
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

        two_factor_service = TwoFactorService(UserRepository(db))
        if not admin.totp_enabled:
            result = two_factor_service.enable_2fa(admin)
            logger.info(f"2FA enabled for admin. TOTP URI: {result['otpauth_uri']}")
        else:
            logger.info("Admin already has 2FA enabled, skipping.")

    except Exception as e:
        logger.error(f"Error when trying to create/verify admin: {e}")
        raise
