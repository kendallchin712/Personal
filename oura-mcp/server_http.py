"""Remote (HTTP) transport for the Oura MCP server.

This wraps the same tools defined in `server.py` but serves them over
Streamable HTTP so the server can run on a public host and be added to
claude.ai as a custom connector — which then works on web, desktop, and the
mobile apps.

Anthropic connects to this server from their cloud, so it must be reachable at
a public HTTPS URL. Because the claude.ai custom-connector UI has no field for
a bearer token, access is gated by an unguessable secret embedded in the URL
path (a "capability URL"): set OURA_MCP_SECRET to a long random string and the
MCP endpoint becomes  /<secret>/mcp  instead of the guessable /mcp.

Environment variables:
  OURA_PERSONAL_ACCESS_TOKEN  (required) your Oura PAT
  OURA_MCP_SECRET             (strongly recommended) random URL secret
  PORT                        (optional) port to bind, default 8000
"""

from __future__ import annotations

import os
import secrets

import uvicorn
from mcp.server.transport_security import TransportSecuritySettings

# Reuse the server instance and all @mcp.tool() registrations from server.py.
from server import mcp


def build_app():
    secret = os.environ.get("OURA_MCP_SECRET", "").strip()
    if not secret:
        # Fail loudly rather than silently exposing an unguessable-free endpoint.
        raise RuntimeError(
            "OURA_MCP_SECRET is not set. Set it to a long random string so the "
            "endpoint is /<secret>/mcp and not publicly guessable. Generate one "
            "with:  python -c \"import secrets; print(secrets.token_urlsafe(32))\""
        )

    path = f"/{secret}/mcp"

    # Anthropic connects server-to-server behind the host's TLS; the secret path
    # is the guard, so DNS-rebinding host checks are not needed here.
    transport_security = TransportSecuritySettings(enable_dns_rebinding_protection=False)

    app = mcp.streamable_http_app(
        streamable_http_path=path,
        host="0.0.0.0",
        transport_security=transport_security,
        # Claude's remote-connector client fetches tools over separate,
        # independently-routed HTTP requests. Stateless + plain-JSON responses
        # avoid depending on a persistent SSE session that a proxy or a
        # cold-starting free-tier host can drop — which otherwise shows up as
        # "This connector has no tools available".
        stateless_http=True,
        json_response=True,
    )
    return app, path


app, _mcp_path = build_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    # Print the path (not including host) so you know what to append to your URL.
    print(f"Oura MCP serving Streamable HTTP at path: {_mcp_path}", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=port)
