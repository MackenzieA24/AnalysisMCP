from __future__ import annotations

from typing import Any

from analysis_mcp.db.mongo import get_database
from analysis_mcp.services.agent_service import get_agent_usage as fetch_agent_usage
from analysis_mcp.services.agent_service import get_agents as fetch_agents
from analysis_mcp.services.agent_service import get_model_usage as fetch_model_usage
from analysis_mcp.utils import safe_tool_call


def get_agents_tool() -> dict[str, str]:
    return {
        "name": "get_agents",
        "description": "List the agents available in the demo database.",
        "schema": "agent-list",
    }


def register(mcp) -> None:
    @mcp.tool()
    @safe_tool_call
    async def get_agents(limit: int = 20) -> dict[str, Any]:
        db = get_database()
        return await fetch_agents(db, limit=limit)

    @mcp.tool()
    @safe_tool_call
    async def get_agent_usage(limit: int = 20) -> dict[str, Any]:
        db = get_database()
        return await fetch_agent_usage(db, limit=limit)

    @mcp.tool()
    @safe_tool_call
    async def get_model_usage(limit: int = 20) -> dict[str, Any]:
        db = get_database()
        return await fetch_model_usage(db, limit=limit)

    return get_agents, get_agent_usage, get_model_usage
