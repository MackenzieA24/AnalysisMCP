from __future__ import annotations

import asyncio
import os
import sys

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

from analysis_mcp.server import main, mcp


def test_server_has_mcp_instance() -> None:
    assert mcp is not None


def test_server_exposes_registered_tools() -> None:
    tools = asyncio.run(mcp.list_tools())
    names = {tool.name for tool in tools}
    assert "get_overview_metrics" in names
    assert "get_users" in names


async def _server_tools_and_tool_result() -> tuple[list[str], dict]:
    env = os.environ.copy()
    src_path = r"C:\Users\aylor\StudioProjects\AnalysisMCP1.1\src"
    env["PYTHONPATH"] = src_path + os.pathsep + env.get("PYTHONPATH", "")
    server = StdioServerParameters(command=sys.executable, args=["-m", "analysis_mcp.server"], env=env)
    async with stdio_client(server) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            response = await session.call_tool("get_overview_metrics", {})
            return [tool.name for tool in tools.tools], response.model_dump()


def test_server_handshake_and_tool_failure_are_structured() -> None:
    names, result = asyncio.run(asyncio.wait_for(_server_tools_and_tool_result(), timeout=15))
    assert "get_overview_metrics" in names
    payload = result.get("structuredContent") or result.get("content") or result
    assert isinstance(payload, dict)
    assert payload.get("ok") is False or "error" in str(payload).lower()


def test_main_runs_without_error() -> None:
    main()
