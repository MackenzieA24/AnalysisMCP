#!/usr/bin/env python3
"""Seed the demo database with deterministic sample data."""

from __future__ import annotations

from analysis_mcp.env import get_settings


def main() -> None:
    settings = get_settings()
    print(f"Seeding demo database: {settings.mongodb_database} @ {settings.mongodb_host}:{settings.mongodb_port}")


if __name__ == "__main__":
    main()
