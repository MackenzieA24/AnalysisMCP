from __future__ import annotations

from typing import Any

from analysis_mcp.db.mongo import get_database
from analysis_mcp.services.metrics_service import get_overview_metrics as get_overview_metrics_service
from analysis_mcp.utils import safe_tool_call


def get_overview_metrics_tool() -> dict[str, str]:
    return {
        "name": "get_overview_metrics",
        "description": "Return the high-level user, conversation, and message totals for the demo database.",
        "schema": "overview-metrics",
    }


def register(mcp) -> None:
    @mcp.tool()
    @safe_tool_call
    async def get_overview_metrics() -> dict[str, Any]:
        db = get_database()
        return await get_overview_metrics_service(db)

    return get_overview_metrics
