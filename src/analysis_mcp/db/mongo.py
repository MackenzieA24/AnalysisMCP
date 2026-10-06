from __future__ import annotations

from urllib.parse import quote_plus

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from analysis_mcp.env import get_settings


def build_mongo_uri() -> str:
    settings = get_settings()
    host = settings.mongodb_host
    port = settings.mongodb_port
    database = settings.mongodb_database

    if settings.mongodb_username and settings.mongodb_password:
        username = quote_plus(settings.mongodb_username)
        password = quote_plus(settings.mongodb_password)
        return (
            f"mongodb://{username}:{password}@{host}:{port}/{database}"
            f"?authSource={quote_plus(settings.mongodb_auth_source)}"
        )

    return f"mongodb://{host}:{port}/{database}"


_client: AsyncIOMotorClient | None = None


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(build_mongo_uri())
    return _client


def get_database() -> AsyncIOMotorDatabase:
    return get_client()[get_settings().mongodb_database]
