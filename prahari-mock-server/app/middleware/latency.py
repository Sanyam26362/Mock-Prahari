import asyncio
import os
import random
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class ArtificialLatencyMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        enabled: bool = True,
        min_ms: int = 150,
        max_ms: int = 450,
    ):
        super().__init__(app)
        self.enabled = os.getenv("MOCK_LATENCY", str(enabled)).lower() in ("true", "1", "yes")
        self.min_ms = int(os.getenv("MOCK_LATENCY_MIN_MS", min_ms))
        self.max_ms = int(os.getenv("MOCK_LATENCY_MAX_MS", max_ms))

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Dynamically evaluate environment configuration
        is_enabled = os.getenv("MOCK_LATENCY", str(self.enabled)).lower() in ("true", "1", "yes")
        min_ms = int(os.getenv("MOCK_LATENCY_MIN_MS", str(self.min_ms)))
        max_ms = int(os.getenv("MOCK_LATENCY_MAX_MS", str(self.max_ms)))

        # Only apply latency to /api/* endpoints, skipping health checks and static files
        if is_enabled and path.startswith("/api") and path != "/api/health":
            delay_seconds = random.uniform(min_ms, max_ms) / 1000.0
            await asyncio.sleep(delay_seconds)

        response = await call_next(request)
        return response
