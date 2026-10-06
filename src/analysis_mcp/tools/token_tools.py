from __future__ import annotations

from typing import Any

from analysis_mcp.db.mongo import get_database
from analysis_mcp.services.token_service import get_token_timeline as fetch_token_timeline
from analysis_mcp.services.token_service import get_token_usage_by_model as fetch_token_usage_by_model
from analysis_mcp.utils import safe_tool_call


def get_token_usage_by_model_tool() -> dict[str, str]:
    return {
        "name": "get_token_usage_by_model",
        "description": "Summarise token usage by model in the demo dataset.",
        "schema": "token-usage",
    }


def register(mcp) -> None:
    @mcp.tool()
    @safe_tool_call
    async def get_token_usage_by_model(limit: int = 20) -> dict[str, Any]:
        db = get_database()
        return await fetch_token_usage_by_model(db, limit=limit)

    @mcp.tool()
    @safe_tool_call
    async def get_token_timeline(granularity: str = "day") -> dict[str, Any]:
        db = get_database()
        return await fetch_token_timeline(db, granularity=granularity)

    return get_token_usage_by_model, get_token_timeline
