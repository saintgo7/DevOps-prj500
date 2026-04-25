"""FastAPI AI Gateway entrypoint."""

from __future__ import annotations

from datetime import UTC, datetime

from fastapi import FastAPI
from pydantic import BaseModel

from .config import settings

app = FastAPI(
    title="SDGI AI Gateway",
    version="0.0.0",
    description="AI gateway for SDG mapping, document extraction, and report drafting.",
)


class HealthResponse(BaseModel):
    status: str
    service: str
    time: str
    model_default: str


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="ai",
        time=datetime.now(UTC).isoformat(),
        model_default=settings.anthropic_model_default,
    )
