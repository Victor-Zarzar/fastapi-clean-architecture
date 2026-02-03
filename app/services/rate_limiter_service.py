from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings

limit_string = f"{settings.RATE_LIMIT_REQUESTS}/{settings.RATE_LIMIT_WINDOW} seconds"

storage_uri = getattr(settings, "RATE_LIMIT_STORAGE_URI", None)

limiter = Limiter(
    key_func=get_remote_address, default_limits=[limit_string], storage_uri=storage_uri
)
