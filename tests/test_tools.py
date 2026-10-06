from __future__ import annotations

from analysis_mcp.tools.metrics_tools import get_overview_metrics_tool


def test_metrics_tool_returns_result() -> None:
    result = get_overview_metrics_tool()
    assert "name" in result
    assert result["name"] == "get_overview_metrics"
