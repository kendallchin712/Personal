# Oura Ring MCP server

A small [MCP](https://modelcontextprotocol.io) server that exposes your Oura
Ring data (via the [Oura API v2](https://cloud.ouraring.com/v2/docs)) as tools,
so Claude can read your sleep, readiness, activity, heart rate, workouts, and
more on demand.

There are two ways to run it:

- **Remote (recommended for you)** — host it publicly and add it once as a
  **custom connector** at claude.ai. It then works on **web, the mobile apps,
  and Claude Desktop**, because Anthropic connects to your server from their
  cloud. This is the only option that reaches your phone and a browser.
- **Local (laptop only)** — run it over stdio for Claude Desktop / Claude Code
  on that one machine. Simple, but it does **not** reach your phone or the web.

Since you want phone + browser + desktop, follow the **Remote** guide below.

---

## ⚠️ First: rotate your token

If you ever pasted your Oura token into a chat or shared it, revoke it at
<https://cloud.ouraring.com/personal-access-tokens> and create a fresh one.
Only ever put the token into a server's environment variables — never into a
chat, a commit, or the connector URL.

---

## Remote setup (phone + web + desktop)

### Step 1 — Get an Oura Personal Access Token (PAT)

1. Go to <https://cloud.ouraring.com/personal-access-tokens> and log in.
2. **Create New Personal Access Token**, name it (e.g. "Claude"), copy it.
3. Keep it secret — it grants read access to your health data.

### Step 2 — Generate a URL secret

The claude.ai connector form has no place for a password, so the server hides
its endpoint behind an unguessable path segment. Generate one:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output — this is your `OURA_MCP_SECRET`. Your MCP endpoint will be
`https://<your-host>/<secret>/mcp`. Anyone without that exact URL gets a 404.

### Step 3 — Deploy the server (Render, free tier)

The repo includes a `Dockerfile` and `render.yaml` blueprint.

1. Push this repo to GitHub (this branch is already on GitHub).
2. Create a free account at <https://render.com> and connect your GitHub.
3. **New → Blueprint**, pick this repo. Render reads `oura-mcp/render.yaml`.
4. When prompted, set the two environment variables (they are **not** stored in
   git):
   - `OURA_PERSONAL_ACCESS_TOKEN` → your Oura PAT from Step 1
   - `OURA_MCP_SECRET` → the secret from Step 2
5. Deploy. Render gives you a public HTTPS URL like
   `https://oura-mcp-xxxx.onrender.com`.

Your connector URL is that host **plus** `/<secret>/mcp`, e.g.
`https://oura-mcp-xxxx.onrender.com/AbC123.../mcp`.

> Any host that runs a Docker container and gives you a public HTTPS URL works
> the same way (Railway, Fly.io, a small VPS). Render's free tier sleeps when
> idle, so the first request after a pause takes ~30s to wake — fine for
> personal use.

### Step 4 — Add it to Claude as a custom connector

Do this **once**, on any device — it then syncs to all your Claude apps
(web, mobile, desktop) because connectors live in your account.

1. Open **claude.ai → Settings → Connectors** (direct link:
   <https://claude.ai/settings/customize-connectors>).
2. **Add custom connector**.
3. Name: `Oura`. URL: your full `https://<host>/<secret>/mcp`.
4. Save. Leave OAuth fields blank (the secret path is your protection).
5. Open a new chat, make sure the **Oura** connector is enabled for the chat,
   and ask away — from your phone, a browser, or Claude Desktop.

> Custom connectors via remote MCP are available on Free, Pro, Max, Team, and
> Enterprise plans (Free is limited to one custom connector).

### Step 5 — Ask Claude

- "What was my average sleep score over the last two weeks?"
- "Show my readiness vs. activity for the past month and flag any dips."
- "How did my resting heart rate trend this week?"

---

## Local setup (laptop only, optional)

If you also want it on Claude Desktop without going through the cloud:

```bash
cd oura-mcp
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Then add to Claude Desktop (**Settings → Developer → Edit Config**), using
absolute paths — a template is in `mcp.example.json`:

```json
{
  "mcpServers": {
    "oura": {
      "command": "/absolute/path/to/oura-mcp/.venv/bin/python",
      "args": ["/absolute/path/to/oura-mcp/server.py"],
      "env": { "OURA_PERSONAL_ACCESS_TOKEN": "your-token-here" }
    }
  }
}
```

Restart Claude Desktop. Or, for Claude Code CLI:

```bash
claude mcp add oura --env OURA_PERSONAL_ACCESS_TOKEN="your-token" \
  -- /abs/path/oura-mcp/.venv/bin/python /abs/path/oura-mcp/server.py
```

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

## Files

| File | Purpose |
|------|---------|
| `server.py` | Tool definitions + Oura API client (used by both transports) |
| `server_http.py` | Remote Streamable-HTTP server (secret-path protected) |
| `Dockerfile` | Container image for hosting the remote server |
| `render.yaml` | One-click Render blueprint |
| `mcp.example.json` | Claude Desktop config template for local use |
| `requirements.txt` | Python dependencies |
| `.env.example` | Token template (copy to `.env`, gitignored) |

## Security notes

- The Oura token is read only from `OURA_PERSONAL_ACCESS_TOKEN`; it is never
  hard-coded, logged, or placed in the URL.
- The remote endpoint is gated by `OURA_MCP_SECRET` in the URL path. Keep that
  URL private (it's like a password). Rotate it by changing the env var.
- `.env` and `*.token` are gitignored. **Never commit your real token.**
- The PAT is read-only for your own account; revoke it anytime from the Oura
  developer portal.
