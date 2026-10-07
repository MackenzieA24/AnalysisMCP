import asyncio
import os
import sys

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def main() -> None:
    env = os.environ.copy()
    src_path = r'C:\Users\aylor\StudioProjects\AnalysisMCP1.1\src'
    env['PYTHONPATH'] = src_path + os.pathsep + env.get('PYTHONPATH', '')
    server = StdioServerParameters(command=sys.executable, args=['-m', 'analysis_mcp.server'], env=env)
    async with stdio_client(server) as (read_stream, write_stream), ClientSession(read_stream, write_stream) as session:
        await session.initialize()
        tools = await session.list_tools()
        names = [tool.name for tool in tools.tools]
        print('TOOLS', names)
        result = await session.call_tool('get_overview_metrics', {})
        print('RESULT', result.model_dump())

asyncio.run(main())
