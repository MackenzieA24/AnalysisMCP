from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class TimelinePoint:
    label: str
    value: int = 0


@dataclass(slots=True)
class OverviewMetrics:
    total_users: int = 0
    total_conversations: int = 0
    total_messages: int = 0
    active_users_7d: int = 0
