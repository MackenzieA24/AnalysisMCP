from __future__ import annotations

from analysis_mcp.db.mongo import build_mongo_uri
from analysis_mcp.env import Settings


def test_settings_defaults() -> None:
    settings = Settings()
    assert settings.mongodb_host == "localhost"
    assert settings.mongodb_database == "analysis_mcp_demo"
    assert settings.mcp_transport == "stdio"


def test_build_mongo_uri_default() -> None:
    uri = build_mongo_uri()
    assert uri == "mongodb://localhost:27017/analysis_mcp_demo"
