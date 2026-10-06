from __future__ import annotations


async def get_token_usage_by_model(db, *, limit: int = 20):
    return {"items": [], "count": 0, "limit": limit}


async def get_token_timeline(db, *, granularity: str = "day"):
    return {"granularity": granularity, "points": []}
