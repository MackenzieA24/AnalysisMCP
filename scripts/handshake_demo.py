from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def run_demo_handshake() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    env = os.environ.copy()
    src_path = str(repo_root / "src")
    env["PYTHONPATH"] = src_path + os.pathsep + env.get("PYTHONPATH", "")

    server = StdioServerParameters(
        command=sys.executable,
        args=["-m", "analysis_mcp.server"],
        env=env,
    )

    async with stdio_client(server) as (read_stream, write_stream), ClientSession(read_stream, write_stream) as session:
        await session.initialize()
        tool_list = await session.list_tools()
        tool_names = [tool.name for tool in tool_list.tools]
        print(f"Tools: {tool_names}")

        result = await session.call_tool("get_overview_metrics", {})
        print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(run_demo_handshake())
