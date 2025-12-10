from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from app.core.config import settings


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    retry_after = int(settings.RATE_LIMIT_WINDOW)

    return JSONResponse(
        status_code=429,
        content={"error": "Too Many Requests", "retry_after_seconds": retry_after},
    )
