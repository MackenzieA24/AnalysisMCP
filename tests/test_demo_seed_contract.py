from __future__ import annotations

from scripts.seed_demo import build_demo_seed, validate_demo_contract


def test_build_demo_seed_has_expected_demo_contract() -> None:
    payload = build_demo_seed()

    assert len(payload["users"]) == 42
    assert len(payload["agents"]) == 6
    assert len(payload["conversations"]) >= 20
    assert len(payload["messages"]) >= 100
    assert len(payload["feedback_events"]) >= 8

    recent_users = [user for user in payload["users"] if user["createdAt"] >= payload["window_start"]]
    assert len(recent_users) == 7

    contract = validate_demo_contract(payload)
    assert contract == []
