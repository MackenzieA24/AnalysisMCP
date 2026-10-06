from __future__ import annotations

from typing import Any

from analysis_mcp.db.mongo import get_database
from analysis_mcp.services.user_service import get_user_details as fetch_user_details
from analysis_mcp.services.user_service import get_users as fetch_users
from analysis_mcp.utils import safe_tool_call


def get_users_tool() -> dict[str, str]:
    return {
        "name": "get_users",
        "description": "List users from the demo dataset with optional limits and filtering.",
        "schema": "user-list",
    }


def register(mcp) -> None:
    @mcp.tool()
    @safe_tool_call
    async def get_users(limit: int = 20, offset: int = 0, role: str | None = None) -> dict[str, Any]:
        db = get_database()
        return await fetch_users(db, limit=limit, offset=offset, role=role)

    @mcp.tool()
    @safe_tool_call
    async def get_user_details(user_id: str) -> dict[str, Any]:
        db = get_database()
        return await fetch_user_details(db, user_id)

    return get_users, get_user_details
