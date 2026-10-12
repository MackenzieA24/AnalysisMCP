from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Anchored to the project root so the server never picks up a .env from
# whatever directory it happens to be launched in.
_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    mongodb_host: str = "localhost"
    mongodb_port: int = 27017
    mongodb_database: str = "analysis_mcp_demo"
    mongodb_username: str | None = None
    mongodb_password: str | None = None
    mongodb_auth_source: str = "admin"
    mcp_transport: str = "stdio"
    mcp_http_port: int = 3100


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
