from __future__ import annotations

from analysis_mcp.tools.metrics_tools import get_overview_metrics_tool
from analysis_mcp.tools.system_tools import get_current_datetime_tool, get_system_status_tool


def test_metrics_tool_returns_result() -> None:
    result = get_overview_metrics_tool()
    assert "name" in result
    assert result["name"] == "get_overview_metrics"


def test_system_tools_are_registered() -> None:
    status = get_system_status_tool()
    current = get_current_datetime_tool()

    assert status["name"] == "get_system_status"
    assert current["name"] == "get_current_datetime"
