# Oura Ring MCP server

A small [MCP](https://modelcontextprotocol.io) server that exposes your Oura
Ring data (via the [Oura API v2](https://cloud.ouraring.com/v2/docs)) as tools,
so Claude can read your sleep, readiness, activity, heart rate, workouts, and
more on demand.

It authenticates with an Oura **Personal Access Token (PAT)** — the simplest
option for a single user (your own account). No OAuth app or hosting required;
the server runs locally over stdio and Claude launches it for you.

---

## 1. Get your Oura Personal Access Token

1. Go to <https://cloud.ouraring.com/personal-access-tokens> and log in.
2. Click **Create New Personal Access Token**, name it (e.g. "Claude"), create it.
3. Copy the token immediately and keep it secret — it grants read access to your
   health data. Treat it like a password.

## 2. Install dependencies

Requires Python 3.10+.

```bash
cd oura-mcp
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Provide the token

Either export it in your shell:

```bash
export OURA_PERSONAL_ACCESS_TOKEN="your-token-here"
```

…or copy `.env.example` to `.env` and paste your token there (the config in
step 4 sets the variable directly, which is what actually matters).

## 4. Register the server with Claude

### Claude Code (CLI)

From the repo root:

```bash
claude mcp add oura \
  --env OURA_PERSONAL_ACCESS_TOKEN="your-token-here" \
  -- /absolute/path/to/oura-mcp/.venv/bin/python /absolute/path/to/oura-mcp/server.py
```

Or add it to a project-scoped `.mcp.json` (see the example block below), then
restart Claude Code.

### Claude Desktop

Open **Settings → Developer → Edit Config** and add an entry under
`mcpServers` (create the file if it doesn't exist):

```json
{
  "mcpServers": {
    "oura": {
      "command": "/absolute/path/to/oura-mcp/.venv/bin/python",
      "args": ["/absolute/path/to/oura-mcp/server.py"],
      "env": {
        "OURA_PERSONAL_ACCESS_TOKEN": "your-token-here"
      }
    }
  }
}
```

Use absolute paths. Restart Claude Desktop after saving. The `oura` tools will
appear in the tools menu.

> **Note:** stdio MCP servers run on the same machine as the Claude client, so
> this works with Claude Code (local/CLI) and Claude Desktop. The claude.ai web
> app only connects to remotely hosted (HTTP/SSE) connectors — to use it there
> you'd need to host this behind an HTTP transport, which is a separate step.

## 5. Ask Claude

Once registered, try:

- "What was my average sleep score over the last two weeks?"
- "Show my readiness vs. activity for the past month and flag any dips."
- "How did my resting heart rate trend this week?"

---

## Available tools

| Tool | Data |
|------|------|
| `get_personal_info` | Profile: age, weight, height, biological sex |
| `get_daily_sleep` | Daily sleep score + contributors |
| `get_daily_readiness` | Daily readiness score + contributors |
| `get_daily_activity` | Steps, calories, MET minutes, activity score |
| `get_daily_stress` | High-stress / recovery-time seconds |
| `get_daily_spo2` | Blood-oxygen (SpO2) averages during sleep |
| `get_daily_resilience` | Resilience level + contributors |
| `get_sleep_periods` | Detailed per-period sleep (stages, HR/HRV series) |
| `get_workouts` | Workouts: type, intensity, calories, timing |
| `get_sessions` | Moment sessions (breathing, meditation, rest) |
| `get_heart_rate` | Time-series heart-rate samples |
| `oura_get` | Escape hatch — call any other v2 endpoint by path |

Date-range tools take ISO dates (`YYYY-MM-DD`) and default to the last 7 days.
`get_heart_rate` uses ISO 8601 datetimes and defaults to the last 24 hours.
Pagination is handled automatically.

## Security

- The token is only ever read from the `OURA_PERSONAL_ACCESS_TOKEN` environment
  variable — it is never hard-coded or logged.
- `.env` and `*.token` are gitignored. **Never commit your real token.**
- The PAT is read-only for your own account; revoke it anytime from the Oura
  developer portal.
