#!/usr/bin/env python3
"""Create the deterministic demo dataset used for the portfolio walkthrough."""

from __future__ import annotations

import asyncio
import random
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from pymongo.errors import PyMongoError

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from analysis_mcp.db.mongo import get_database


def build_demo_seed() -> dict[str, Any]:
    """Return the seed payload used by the demo and verify scripts."""
    today = datetime.now(UTC).date()
    window_start = today - timedelta(days=89)
    rng = random.Random(20261006)

    first_names = [
        "Avery", "Mateo", "Sienna", "Julian", "Priya", "Omar", "Elena", "Jalen",
        "Harper", "Lucas", "Nadia", "Darius", "Camila", "Theo", "Zuri", "Arjun",
        "Layla", "Marco", "Rhea", "Samir", "Noor", "Oscar", "Sofia", "Devon",
        "Iris", "Adrian", "Keira", "Rafael", "Amara", "Noel", "Talia", "Ethan",
        "Lena", "Victor", "Maya", "Dylan", "Cora", "Nolan", "Anika", "Ibrahim",
        "Selene", "Kian", "Alina", "Gabriel",
    ]
    last_names = [
        "Liu", "Moreno", "Patel", "Stone", "Bass", "Hernandez", "Rao", "Nguyen",
        "Santos", "Walters", "Bishop", "Hughes", "Choi", "Rivera", "Keller", "Ibarra",
        "Mendez", "Parikh", "Osei", "Garcia", "Bennett", "Rossi", "Nolan", "Singh",
        "Foster", "Mora", "Sharma", "Khan", "Ochoa", "Bautista", "Adebayo", "Quinn",
        "Murphy", "Chambers", "Ali", "Jensen", "Vargas", "Wells", "Norris", "Hale",
        "Mendoza", "Sanchez",
    ]

    users: list[dict[str, Any]] = []
    for index in range(42):
        first_name = first_names[index % len(first_names)]
        last_name = last_names[index % len(last_names)]
        username = f"{first_name.lower()}{index + 1}"
        created_at = today - timedelta(days=90 + index) if index >= 7 else today - timedelta(days=rng.randint(1, 89))
        users.append(
            {
                "_id": f"user-{index + 1:02d}",
                "name": f"{first_name} {last_name}",
                "username": username,
                "email": f"{username}@northstarlabs.io",
                "role": "analyst" if index % 2 == 0 else "product",
                "createdAt": created_at.isoformat(),
            }
        )

    agents = [
        {
            "id": "agent-atlas-forecast",
            "name": "Atlas Forecast Monitor",
            "description": "Tracks pipeline health and projected revenue shifts.",
            "provider": "Anthropic",
            "model": "claude-3.5-sonnet",
            "tools": ["search", "summarize"],
            "author": "northstar-demo",
        },
        {
            "id": "agent-northstar-policy",
            "name": "Northstar Policy Copilot",
            "description": "Reviews process drift and control exceptions.",
            "provider": "Anthropic",
            "model": "claude-3-opus",
            "tools": ["search", "compare"],
            "author": "northstar-demo",
        },
        {
            "id": "agent-signal-insights",
            "name": "Signal Insights Bot",
            "description": "Finds user engagement and adoption anomalies.",
            "provider": "OpenAI",
            "model": "gpt-4o-mini",
            "tools": ["aggregate", "chart"],
            "author": "northstar-demo",
        },
        {
            "id": "agent-qa-rapid",
            "name": "Rapid Support Coach",
            "description": "Answers product issues and customer support questions.",
            "provider": "OpenAI",
            "model": "gpt-4o",
            "tools": ["answer", "search"],
            "author": "northstar-demo",
        },
        {
            "id": "agent-contract-guard",
            "name": "Contract Guard",
            "description": "Highlights legal, commercial, and renewal exposure.",
            "provider": "OpenAI",
            "model": "gpt-4.1",
            "tools": ["compare", "risk"],
            "author": "northstar-demo",
        },
        {
            "id": "agent-board-briefing",
            "name": "Board Briefing Studio",
            "description": "Creates executive summaries and performance narratives.",
            "provider": "Anthropic",
            "model": "claude-3.5-haiku",
            "tools": ["report", "chart"],
            "author": "northstar-demo",
        },
    ]

    conversations: list[dict[str, Any]] = []
    titles = [
        "Q4 launch readiness",
        "Northstar policy review",
        "Customer retention pulse",
        "Commercial risk watchlist",
        "Onboarding acceleration plan",
        "Usage trend anomaly review",
        "Market response brief",
        "Partner rollout dashboard",
        "Executive scorecard update",
        "Support escalation sweep",
    ]
    for index in range(24):
        user = users[index % len(users)]
        agent = agents[index % len(agents)]
        created_at = today - timedelta(days=(index * 3) % 180, hours=index % 20)
        updated_at = created_at + timedelta(hours=2 + (index % 6))
        conversations.append(
            {
                "conversationId": f"conv-{index + 1:02d}",
                "user": user["username"],
                "title": f"{titles[index % len(titles)]} {index + 1}",
                "agent_id": agent["id"],
                "endpoint": "claude_desktop",
                "model": agent["model"],
                "createdAt": created_at.isoformat(),
                "updatedAt": updated_at.isoformat(),
            }
        )

    messages: list[dict[str, Any]] = []
    feedback_events: list[dict[str, Any]] = []
    assistant_index = 0
    contract_review_warning_sent = False
    for conversation_index, conversation in enumerate(conversations):
        for message_index in range(5):
            message_id = f"msg-{conversation_index + 1}-{message_index + 1}"
            is_user_message = message_index % 2 == 0
            sender = "user" if is_user_message else "assistant"
            created_at = (datetime.fromisoformat(conversation["createdAt"]) + timedelta(hours=message_index * 3)).isoformat()
            message = {
                "_id": message_id,
                "messageId": message_id,
                "conversationId": conversation["conversationId"],
                "user": conversation["user"],
                "sender": sender,
                "isCreatedByUser": is_user_message,
                "text": f"{conversation['title']} message {message_index + 1}",
                "content": f"{conversation['title']} message {message_index + 1}",
                "model": None if is_user_message else conversation["model"],
                "tokenCount": 120 + message_index * 18 if not is_user_message else None,
                "createdAt": created_at,
            }
            messages.append(message)
            if not is_user_message and (assistant_index % 6 == 0 or (conversation["agent_id"] == "agent-contract-guard" and not contract_review_warning_sent)):
                if conversation["agent_id"] == "agent-contract-guard":
                    rating = "thumbs-down"
                    contract_review_warning_sent = True
                else:
                    rating = "thumbs-up"
                feedback_events.append(
                    {
                        "messageId": message_id,
                        "conversationId": conversation["conversationId"],
                        "user": conversation["user"],
                        "rating": rating,
                        "createdAt": created_at,
                    }
                )
            if not is_user_message:
                assistant_index += 1

    return {
        "window_start": window_start.isoformat(),
        "users": users,
        "agents": agents,
        "conversations": conversations,
        "messages": messages,
        "feedback_events": feedback_events,
    }


def validate_demo_contract(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    users = payload.get("users", [])
    agents = payload.get("agents", [])
    conversations = payload.get("conversations", [])
    messages = payload.get("messages", [])
    feedback_events = payload.get("feedback_events", [])
    window_start = payload.get("window_start")

    if len(users) != 42:
        errors.append(f"Expected 42 users, found {len(users)}")
    recent_users = [user for user in users if user.get("createdAt", "") >= window_start]
    if len(recent_users) != 7:
        errors.append(f"Expected 7 users in the 90-day window, found {len(recent_users)}")
    if len(agents) != 6:
        errors.append(f"Expected 6 agents, found {len(agents)}")
    if len(conversations) < 20:
        errors.append(f"Expected at least 20 conversations, found {len(conversations)}")
    if len(messages) < 100:
        errors.append(f"Expected at least 100 messages, found {len(messages)}")
    if len(feedback_events) < 8:
        errors.append(f"Expected at least 8 feedback events, found {len(feedback_events)}")

    assistant_messages = [msg for msg in messages if msg.get("sender") == "assistant"]
    if assistant_messages:
        feedback_ratio = len(feedback_events) / len(assistant_messages)
        if not 0.12 <= feedback_ratio <= 0.20:
            errors.append(
                "Feedback ratio should be roughly 12% to 20% of assistant messages; "
                f"found {feedback_ratio:.2%}."
            )

    contract_reviewer = next((agent for agent in agents if agent.get("name") in {"Contract Reviewer", "Contract Guard"}), None)
    if contract_reviewer is None:
        errors.append("Missing the required contract-risk agent in the seed dataset.")
    else:
        contract_conversations = [
            conversation for conversation in conversations if conversation.get("agent_id") == contract_reviewer["id"]
        ]
        contract_conversation_count = len(contract_conversations)
        if contract_conversation_count == 0:
            errors.append("The contract-risk agent does not appear in any conversation.")
        contract_downvotes = [
            event for event in feedback_events if event.get("rating") == "thumbs-down" and any(
                event.get("conversationId") == conversation.get("conversationId")
                for conversation in contract_conversations
            )
        ]
        if len(contract_downvotes) == 0:
            errors.append("The contract-risk agent has no thumbs-down feedback events.")

    return errors


async def seed_demo_database(db=None) -> dict[str, Any]:
    """Insert the deterministic demo dataset into the MongoDB database."""
    if db is None:
        db = get_database()

    try:
        await db.command("ping")
    except PyMongoError as exc:  # pragma: no cover - environment-specific connection check
        return {
            "status": "skipped",
            "message": "Demo MongoDB is not running. Start it with `docker compose -f docker-compose.demo.yml up -d`.",
            "error": str(exc),
        }

    payload = build_demo_seed()
    for collection_name in ("users", "conversations", "messages", "agents"):
        await db[collection_name].delete_many({})

    if payload.get("users"):
        await db.users.insert_many(payload["users"])
    if payload.get("agents"):
        await db.agents.insert_many(payload["agents"])
    if payload.get("conversations"):
        await db.conversations.insert_many(payload["conversations"])
    if payload.get("messages"):
        await db.messages.insert_many(payload["messages"])

    return {
        "status": "seeded",
        "users": len(payload["users"]),
        "agents": len(payload["agents"]),
        "conversations": len(payload["conversations"]),
        "messages": len(payload["messages"]),
    }


def main() -> None:
    result = asyncio.run(seed_demo_database())
    if result.get("status") == "skipped":
        print(result["message"])
        return
    print(
        "Seeded demo data: "
        f"{result['users']} users, {result['agents']} agents, "
        f"{result['conversations']} conversations, {result['messages']} messages"
    )


if __name__ == "__main__":
    main()
