from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from .auth import validate_token
from .rate_limiter import check_rate_limits


class GatewayMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        public_paths = [
            "/health",
            "/auth/login",
            "/auth/signup",
            "/docs",
            "/openapi.json",
            "/redoc"
        ]
        if request.url.path in public_paths:
            return await call_next(request)

        # 1. REQUEST INTERCEPTOR: Auth check
        is_valid, user_id, api_key = validate_token(request)
        if not is_valid:
            return JSONResponse(
                status_code=401,
                content={"detail": "Unauthorized: Invalid or missing token"},
            )

        # If valid -> extract user_id and api_key, attach to request state
        request.state.user_id = user_id
        request.state.api_key = api_key

        # 2. REDIS RATE LIMITING — SLIDING WINDOW
        client_ip = request.client.host if request.client else "127.0.0.1"
        is_allowed, error_detail, retry_after = await check_rate_limits(
            client_ip, api_key
        )

        if not is_allowed:
            return JSONResponse(
                status_code=429,
                content={"detail": error_detail, "retry_after": retry_after},
                headers={"Retry-After": str(retry_after)},
            )

        # Pass request through
        return await call_next(request)
