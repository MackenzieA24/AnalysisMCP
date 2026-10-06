# AnalysisMCP

A demo-focused Model Context Protocol (MCP) analytics server built for a single seeded MongoDB database and the Claude Desktop workflow.

## Purpose

This project keeps the original AnalysisMCP tool contracts while removing the extra multi-tenant and LibreChat-specific deployment layers. The result is a clean portfolio-friendly project for a local Claude Desktop demonstration.

## Quick start

1. Create a virtual environment.
2. Install dependencies:
   `pip install -e .[dev]`
3. Copy `.env.example` to `.env` and adjust values if needed.
4. Run the demo seed script or start the MCP server from the local client config.

## Project structure

- `src/analysis_mcp/` — package code
- `scripts/` — demo setup and publishing checks
- `tests/` — smoke and configuration checks
- `demo/` — Claude Desktop config examples
