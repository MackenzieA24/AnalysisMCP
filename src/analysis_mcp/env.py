from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
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
