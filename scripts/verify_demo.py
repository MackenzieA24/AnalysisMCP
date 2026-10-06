#!/usr/bin/env python3
"""Validate the seeded demo database against the Phase 4 contract."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from analysis_mcp.db.mongo import get_database
from scripts.seed_demo import build_demo_seed, validate_demo_contract


async def verify_demo_database(db=None) -> tuple[bool, list[str], dict[str, Any]]:
    """Return whether the current database satisfies the demo contract."""
    payload = build_demo_seed()
    errors = validate_demo_contract(payload)

    if db is None:
        db = get_database()

    try:
        await db.command("ping")
    except Exception as exc:  # pragma: no cover - environment-specific connection check
        return False, [f"MongoDB unavailable: {exc}"], payload

    counts = {
        "users": await db.users.count_documents({}),
        "agents": await db.agents.count_documents({}),
        "conversations": await db.conversations.count_documents({}),
        "messages": await db.messages.count_documents({}),
    }

    expected = {
        "users": 42,
        "agents": 6,
        "conversations": 24,
        "messages": 120,
    }
    for name, expected_value in expected.items():
        actual_value = counts.get(name)
        if actual_value != expected_value:
            errors.append(f"Expected {expected_value} {name}, found {actual_value}")

    return not errors, errors, payload


def main() -> int:
    success, errors, payload = asyncio.run(verify_demo_database())
    if not success:
        print("Demo verification failed:")
        for item in errors:
            print(f"- {item}")
        return 1

    print("Demo verification passed.")
    print(
        "Seed payload: "
        f"{len(payload['users'])} users, {len(payload['agents'])} agents, "
        f"{len(payload['conversations'])} conversations, {len(payload['messages'])} messages"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
