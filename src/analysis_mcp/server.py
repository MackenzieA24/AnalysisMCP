from __future__ import annotations

import sys
from importlib.metadata import version
from typing import Literal

from mcp.server.mcpserver import MCPServer

from analysis_mcp.env import get_settings
from analysis_mcp.tools.agent_tools import register as register_agents
from analysis_mcp.tools.conversation_tools import register as register_conversations
from analysis_mcp.tools.metrics_tools import register as register_metrics
from analysis_mcp.tools.system_tools import register as register_system
from analysis_mcp.tools.token_tools import register as register_tokens
from analysis_mcp.tools.user_tools import register as register_users

# mcp 2.x reports an empty server version unless one is passed explicitly
mcp = MCPServer("analysis-mcp", version=version("analysis-mcp"))

register_system(mcp)
register_metrics(mcp)
register_users(mcp)
register_conversations(mcp)
register_agents(mcp)
register_tokens(mcp)


def main(run_server: bool = False) -> None:
    settings = get_settings()
    # stderr only: in stdio mode stdout is the JSON-RPC channel
    print(f"Starting AnalysisMCP in {settings.mcp_transport} mode", file=sys.stderr)
    print(
        f"MongoDB target: {settings.mongodb_host}:{settings.mongodb_port}/{settings.mongodb_database}",
        file=sys.stderr,
    )
    if run_server:
        if settings.mcp_transport == "stdio":
            mcp.run(transport="stdio")
        else:
            # mcp 2.x takes network settings on run() rather than the constructor
            transport: Literal["sse", "streamable-http"] = (
                "sse" if settings.mcp_transport == "sse" else "streamable-http"
            )
            mcp.run(transport=transport, port=settings.mcp_http_port)


if __name__ == "__main__":
    main(run_server=True)
