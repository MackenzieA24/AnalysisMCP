from __future__ import annotations

from pathlib import Path

import pytest

from analysis_mcp.db.mongo import build_mongo_uri, close_client, get_database
from analysis_mcp.env import Settings, get_settings


def test_settings_defaults() -> None:
    settings = Settings()
    assert settings.mongodb_host == "localhost"
    assert settings.mongodb_database == "analysis_mcp_demo"
    assert settings.mcp_transport == "stdio"


def test_settings_ignore_env_file_in_working_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / ".env").write_text("MONGODB_HOST=not-the-demo-host\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("MONGODB_HOST", raising=False)

    assert Settings().mongodb_host == "localhost"


def test_build_mongo_uri_default() -> None:
    uri = build_mongo_uri()
    assert uri == "mongodb://localhost:27017/analysis_mcp_demo"


def test_build_mongo_uri_with_credentials() -> None:
    original = get_settings()
    original.mongodb_username = "demo-user"
    original.mongodb_password = "demo-pass"
    uri = build_mongo_uri()
    assert uri == "mongodb://demo-user:demo-pass@localhost:27017/analysis_mcp_demo?authSource=admin"


def test_close_client_closes_current_connection(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeClient:
        def __init__(self) -> None:
            self.closed = False

        def close(self) -> None:
            self.closed = True

    fake_client = FakeClient()
    monkeypatch.setattr("analysis_mcp.db.mongo._client", fake_client)

    close_client()

    assert fake_client.closed is True


def test_get_database_uses_configured_name(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeDatabase:
        pass

    class FakeClient:
        def __getitem__(self, name: str) -> FakeDatabase:
            assert name == "analysis_mcp_demo"
            return FakeDatabase()

    fake_client = FakeClient()
    monkeypatch.setattr("analysis_mcp.db.mongo._client", fake_client)

    database = get_database()

    assert isinstance(database, FakeDatabase)
