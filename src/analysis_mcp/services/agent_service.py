from __future__ import annotations


async def get_agents(db, *, limit: int = 20):
    return {"items": [], "count": 0, "limit": limit}


async def get_agent_usage(db, *, limit: int = 20):
    return {"items": [], "count": 0, "limit": limit}


async def get_model_usage(db, *, limit: int = 20):
    return {"items": [], "count": 0, "limit": limit}
