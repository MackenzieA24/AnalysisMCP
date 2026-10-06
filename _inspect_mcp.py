import inspect
from mcp.server.fastmcp import FastMCP
print(inspect.signature(FastMCP.run))
print(inspect.getsource(FastMCP.run))
