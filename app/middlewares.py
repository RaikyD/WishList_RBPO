import os
import time
import uuid
from collections import defaultdict, deque
from typing import Deque, Dict

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

RATE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        rid = request.headers.get("X-Request-Id") or str(uuid.uuid4())
        response: Response = await call_next(request)
        response.headers["X-Request-Id"] = rid
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.window: Dict[str, Deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        if request.method == "GET":
            # Получаем текущий лимит из переменной окружения
            current_rate = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
            now = time.time()
            # Используем IP адрес клиента или заглушку для тестов
            key = getattr(request.client, "host", "test") if request.client else "test"
            q = self.window[key]
            while q and now - q[0] > 60:
                q.popleft()
            if len(q) >= current_rate:
                return Response(
                    status_code=429,
                    content='{"error":{"code":"too_many_requests","message":"rate limit"}}',
                    media_type="application/json",
                )
            q.append(now)
        return await call_next(request)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        # Minimal safe defaults for APIs
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        # Restrictive permissions policy (formerly feature-policy)
        response.headers.setdefault(
            "Permissions-Policy",
            "camera=(), microphone=(), geolocation=()",
        )
        # Conservative CSP for JSON API (no inline/script allowed)
        response.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'none'; frame-ancestors 'none'; base-uri 'none'",
        )
        # HSTS is harmless in tests (served over HTTP), but okay to send
        response.headers.setdefault(
            "Strict-Transport-Security",
            "max-age=31536000; includeSubDomains",
        )
        return response
