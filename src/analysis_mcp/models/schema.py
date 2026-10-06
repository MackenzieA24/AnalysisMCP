from __future__ import annotations

from typing import TypedDict


class UserRecord(TypedDict, total=False):
    _id: str
    name: str
    username: str
    email: str
    role: str


class MessageRecord(TypedDict, total=False):
    _id: str
    conversationId: str
    user: str
    sender: str
    isCreatedByUser: bool
    text: str
    content: str
    model: str
    tokenCount: int | None
    createdAt: str


class ConversationRecord(TypedDict, total=False):
    conversationId: str
    user: str
    title: str
    agent_id: str
    endpoint: str
    model: str
    createdAt: str
    updatedAt: str
