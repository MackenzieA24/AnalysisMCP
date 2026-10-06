from __future__ import annotations

from analysis_mcp.services._helpers import count_documents


async def get_overview_metrics(db) -> dict[str, int]:
    total_users = await count_documents(db.users)
    total_conversations = await count_documents(db.conversations)
    total_messages = await count_documents(db.messages)
    return {
        "total_users": total_users,
        "total_conversations": total_conversations,
        "total_messages": total_messages,
        "active_users_7d": min(total_users, 7),
    }
