from __future__ import annotations

from typing import Any


def build_date_filter(start_date: str | None = None, end_date: str | None = None, field: str = "createdAt") -> dict[str, Any]:
    if not start_date and not end_date:
        return {}

    filter_map: dict[str, Any] = {}
    if start_date:
        filter_map["$gte"] = start_date
    if end_date:
        filter_map["$lte"] = end_date
    return {field: filter_map}


async def count_documents(collection) -> int:
    if collection is None:
        return 0

    try:
        return await collection.count_documents({})
    except (AttributeError, TypeError):
        pass

    try:
        cursor = collection.aggregate([{"$count": "count"}])
        if hasattr(cursor, "to_list"):
            items = await cursor.to_list(length=1)
        else:
            items = await cursor
    except TypeError:
        items = await collection.aggregate([{"$count": "count"}])

    return _first_count(items)


def _first_count(cursor) -> int:
    try:
        first = next(iter(cursor))
    except StopIteration:
        return 0
    if isinstance(first, dict):
        return int(first.get("count", 0))
    return 0
