from __future__ import annotations

from typing import Any

from analysis_mcp.db.mongo import get_database
from analysis_mcp.services.conversation_service import (
    get_conversation_detail as fetch_conversation_detail,
)
from analysis_mcp.services.conversation_service import get_conversations as fetch_conversations
from analysis_mcp.services.conversation_service import (
    search_conversations as fetch_search_conversations,
)
from analysis_mcp.utils import safe_tool_call


def get_conversations_tool() -> dict[str, str]:
    return {
        "name": "get_conversations",
        "description": "Return recent conversations from the demo dataset.",
        "schema": "conversation-list",
    }


def register(mcp) -> None:
    @mcp.tool()
    @safe_tool_call
    async def get_conversations(limit: int = 20, offset: int = 0) -> dict[str, Any]:
        db = get_database()
        return await fetch_conversations(db, limit=limit, offset=offset)

    @mcp.tool()
    @safe_tool_call
    async def get_conversation_detail(conversation_id: str) -> dict[str, Any]:
        db = get_database()
        return await fetch_conversation_detail(db, conversation_id)

    @mcp.tool()
    @safe_tool_call
    async def search_conversations(term: str, limit: int = 20) -> dict[str, Any]:
        db = get_database()
        return await fetch_search_conversations(db, term, limit=limit)
