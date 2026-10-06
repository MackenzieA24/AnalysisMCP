from __future__ import annotations


async def get_users(db, *, limit: int = 20, offset: int = 0, role: str | None = None):
    query = {"role": role} if role else {}
    items = list(db.users.find(query, sort=[("createdAt", -1)], skip=offset, limit=limit))
    return {"items": items, "count": len(items), "offset": offset, "limit": limit}


async def get_user_details(db, user_id: str):
    return db.users.find_one({"_id": user_id})


async def get_new_users(db, *, days: int = 30):
    return {"count": 0, "days": days, "users": []}
