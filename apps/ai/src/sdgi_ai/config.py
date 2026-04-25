"""AI Gateway settings (env-driven)."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SDGI_AI_", env_file=".env", extra="ignore")

    anthropic_api_key: str = ""
    anthropic_model_default: str = "claude-sonnet-4-6"
    anthropic_model_report: str = "claude-opus-4-7"
    anthropic_model_summary: str = "claude-haiku-4-5-20251001"
    log_level: str = "INFO"


settings = Settings()
