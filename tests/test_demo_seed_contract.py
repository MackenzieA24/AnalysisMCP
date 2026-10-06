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


def test_build_demo_seed_uses_fresh_demo_identity() -> None:
    payload = build_demo_seed()
    legacy_names = {"Ava", "Noah", "Mila", "Leo", "Zoe", "Eli", "Nia", "Owen", "Ivy", "Kai"}
    legacy_titles = {"Weekly adoption summary", "Policy review", "Customer health check", "Contract red flags"}

    names = {user["name"].split()[0] for user in payload["users"]}
    titles = {conversation["title"] for conversation in payload["conversations"]}

    assert names.isdisjoint(legacy_names)
    assert titles.isdisjoint(legacy_titles)
