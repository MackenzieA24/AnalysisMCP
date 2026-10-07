# AnalysisMCP

AnalysisMCP is a lightweight MCP analytics demo built to show how a local AI client can query a structured dataset, interpret the results, and present the findings in natural language.


## What the server exposes

The project exposes a fixed set of MCP tools for user, conversation, agent, token, and high-level operational analytics.

### Core tools

- System: `get_system_status`, `get_current_datetime`
- Users: `get_users`, `get_user_details`, `get_new_users`
- Conversations: `get_conversations`, `get_conversation_detail`, `get_conversations_with_feedback`, `search_conversations`, `get_conversation_tool_calls`
- Metrics: `get_overview_metrics`
- Agents and models: `get_agents`, `get_agent_usage`, `get_model_usage`
- Tokens: `get_token_usage_by_model`, `get_token_timeline`

The design deliberately keeps the model in charge of interpretation. Tools return structured JSON; the LLM decides how to compare, explain, and summarize the results.

## Quick start

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
. .venv/bin/activate
```

On Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install project dependencies

```bash
pip install -e '.[dev]'
```

### 3. Start the demo MongoDB instance

```bash
docker compose -f docker-compose.demo.yml up -d
```

### 4. Seed the demo database

```bash
python scripts/seed_demo.py
```

### 5. Verify the contract and handshake

```bash
python scripts/verify_demo.py
python scripts/handshake_demo.py
```

### 6. Run the project through Claude Desktop

Use the example config in `demo/` as the starting point, then point Claude Desktop at this repo checkout and the local Python executable.


