from __future__ import annotations

import asyncio

from analysis_mcp.services._helpers import build_date_filter
from analysis_mcp.services.metrics_service import get_overview_metrics


class FakeCollection:
    def __init__(self, *docs):
        self.docs = list(docs)

    async def aggregate(self, pipeline):
        if pipeline and pipeline[0].get("$count") == "count":
            return [{"count": len(self.docs)}]
        return list(self.docs)

    async def find_one(self, query):
        for item in self.docs:
            if all(item.get(key) == value for key, value in query.items()):
                return item
        return None

    def find(self, query=None, sort=None, skip=0, limit=0):
        items = list(self.docs)
        if query:
            items = [item for item in items if all(item.get(key) == value for key, value in query.items())]
        if sort:
            reverse = sort[0][1] == -1
            items = sorted(items, key=lambda item: item.get(sort[0][0], 0), reverse=reverse)
        if skip:
            items = items[skip:]
        if limit:
            items = items[:limit]
        return items


class FakeDatabase:
    def __init__(self):
        self.users = FakeCollection({"_id": "u1", "name": "Alice"}, {"_id": "u2", "name": "Bob"})
        self.conversations = FakeCollection({"_id": "c1"}, {"_id": "c2"}, {"_id": "c3"})
        self.messages = FakeCollection({"_id": "m1"}, {"_id": "m2"}, {"_id": "m3"}, {"_id": "m4"})


def test_build_date_filter() -> None:
    result = build_date_filter("2024-01-01", "2024-01-31")
    assert result == {"createdAt": {"$gte": "2024-01-01", "$lte": "2024-01-31"}}


def test_get_overview_metrics() -> None:
    db = FakeDatabase()
    result = asyncio.run(get_overview_metrics(db))
    assert result["total_users"] == 2
    assert result["total_conversations"] == 3
    assert result["total_messages"] == 4
