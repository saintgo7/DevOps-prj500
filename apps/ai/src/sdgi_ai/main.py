"""FastAPI AI Gateway entrypoint."""

from __future__ import annotations

import logging
import sys
import uuid
from datetime import UTC, datetime
from typing import Any

import structlog
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel

from .config import settings


def _configure_logging() -> None:
    """Configure structlog to emit JSON logs with the standard SDGI fields."""
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=settings.log_level.upper(),
    )
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.log_level.upper(), logging.INFO),
        ),
        cache_logger_on_first_use=True,
    )


_configure_logging()
log = structlog.get_logger().bind(service="ai", env="dev")

app = FastAPI(
    title="SDGI AI Gateway",
    version="0.0.0",
    description="AI gateway for SDG mapping, document extraction, and report drafting.",
)


@app.middleware("http")
async def request_id_middleware(request: Request, call_next: Any) -> Response:
    incoming = request.headers.get("x-request-id")
    request_id = incoming if incoming and 8 <= len(incoming) <= 128 else uuid.uuid4().hex
    structlog.contextvars.bind_contextvars(request_id=request_id, path=request.url.path)
    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    structlog.contextvars.clear_contextvars()
    return response


class HealthResponse(BaseModel):
    status: str
    service: str
    time: str
    model_default: str


class ReadinessResponse(BaseModel):
    status: str
    checks: dict[str, str]
    time: str


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="ai",
        time=datetime.now(UTC).isoformat(),
        model_default=settings.anthropic_model_default,
    )


@app.get("/ready", response_model=ReadinessResponse)
async def ready() -> ReadinessResponse:
    # No external deps required for the AI gateway baseline; future readiness
    # checks (Anthropic API reachability, prompt-cache health) plug in here.
    return ReadinessResponse(
        status="ok",
        checks={"self": "ok"},
        time=datetime.now(UTC).isoformat(),
    )
