from __future__ import annotations

from analysis_mcp.env import get_settings


def main() -> None:
    settings = get_settings()
    print(f"Starting AnalysisMCP in {settings.mcp_transport} mode")
    print(f"MongoDB target: {settings.mongodb_host}:{settings.mongodb_port}/{settings.mongodb_database}")


if __name__ == "__main__":
    main()
