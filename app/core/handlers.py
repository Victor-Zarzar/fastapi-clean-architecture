from slowapi.errors import RateLimitExceeded
from starlette.requests import Request
from starlette.responses import JSONResponse


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    retry_after = getattr(exc, "retry_after", None)

    payload = {
        "error": "Too Many Requests",
        "detail": str(exc),
        "retry_after_seconds": int(retry_after) if retry_after is not None else 60,
    }

    headers = {}
    if payload["retry_after_seconds"] is not None:
        headers["Retry-After"] = str(payload["retry_after_seconds"])

    return JSONResponse(status_code=429, content=payload, headers=headers)
