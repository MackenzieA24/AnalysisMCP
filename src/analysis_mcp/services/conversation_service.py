from __future__ import annotations


async def get_conversations(db, *, limit: int = 20, offset: int = 0):
    items = list(db.conversations.find({}, sort=[("updatedAt", -1)], skip=offset, limit=limit))
    return {"items": items, "count": len(items), "offset": offset, "limit": limit}


async def get_conversation_detail(db, conversation_id: str):
    return db.conversations.find_one({"_id": conversation_id})


async def search_conversations(db, term: str, *, limit: int = 20):
    return {"term": term, "items": [], "count": 0, "limit": limit}


async def get_conversations_with_feedback(db, *, limit: int = 20):
    return {"items": [], "count": 0, "limit": limit}


async def get_conversation_tool_calls(db, conversation_id: str):
    return {"conversation_id": conversation_id, "items": []}
