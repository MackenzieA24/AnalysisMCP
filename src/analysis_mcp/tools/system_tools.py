from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pymongo.errors import PyMongoError

from analysis_mcp.db.mongo import get_database
from analysis_mcp.env import get_settings
from analysis_mcp.utils import safe_tool_call


def get_system_status_tool() -> dict[str, str]:
    return {
        "name": "get_system_status",
        "description": "Return the local AnalysisMCP server status and the configured MongoDB demo database connection details.",
        "schema": "system-status",
    }


def get_current_datetime_tool() -> dict[str, str]:
    return {
        "name": "get_current_datetime",
        "description": "Return the current UTC timestamp for the local AnalysisMCP demo environment.",
        "schema": "datetime",
    }


def register(mcp) -> None:
    @mcp.tool()
    @safe_tool_call
    async def get_system_status() -> dict[str, Any]:
        settings = get_settings()
        status = {
            "ok": True,
            "server": "analysis-mcp",
            "transport": settings.mcp_transport,
            "database": settings.mongodb_database,
            "host": settings.mongodb_host,
            "port": settings.mongodb_port,
            "status": "ready",
        }

        try:
            db = get_database()
            await db.command("ping")
        except (ConnectionError, OSError, PyMongoError, TimeoutError) as exc:  # pragma: no cover - safety layer for MCP tools
            status["ok"] = False
            status["status"] = "error"
            status["error"] = str(exc)

        return status

    @mcp.tool()
    @safe_tool_call
    async def get_current_datetime() -> dict[str, str]:
        return {
            "datetime": datetime.now(UTC).isoformat(),
            "timezone": "UTC",
        }
