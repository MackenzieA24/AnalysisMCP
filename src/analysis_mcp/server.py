from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from analysis_mcp.env import get_settings
from analysis_mcp.tools.agent_tools import register as register_agents
from analysis_mcp.tools.conversation_tools import register as register_conversations
from analysis_mcp.tools.metrics_tools import register as register_metrics
from analysis_mcp.tools.system_tools import register as register_system
from analysis_mcp.tools.token_tools import register as register_tokens
from analysis_mcp.tools.user_tools import register as register_users

mcp = FastMCP("analysis-mcp")

register_system(mcp)
register_metrics(mcp)
register_users(mcp)
register_conversations(mcp)
register_agents(mcp)
register_tokens(mcp)


def main(run_server: bool = False) -> None:
    settings = get_settings()
    print(f"Starting AnalysisMCP in {settings.mcp_transport} mode")
    print(f"MongoDB target: {settings.mongodb_host}:{settings.mongodb_port}/{settings.mongodb_database}")
    if run_server:
        mcp.run(transport=settings.mcp_transport)


if __name__ == "__main__":
    main(run_server=True)
