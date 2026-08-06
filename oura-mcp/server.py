"""Oura Ring MCP server.

Exposes your Oura Ring data (via the Oura API v2) as MCP tools so Claude can
query it on demand. Authentication uses an Oura Personal Access Token (PAT)
supplied through the OURA_PERSONAL_ACCESS_TOKEN environment variable.

Create a PAT at https://cloud.ouraring.com/personal-access-tokens
API reference: https://cloud.ouraring.com/v2/docs
"""

from __future__ import annotations

import json
import os
from datetime import date, timedelta
from typing import Any

import httpx

# The high-level server class was renamed FastMCP -> MCPServer in the mcp 2.0
# SDK. Support both so this runs on 1.x and 2.x installs alike.
try:
    from mcp.server import MCPServer as _Server  # mcp >= 2.0
except ImportError:  # pragma: no cover - older SDKs
    from mcp.server.fastmcp import FastMCP as _Server  # mcp 1.x

API_BASE = "https://api.ouraring.com/v2/usercollection"
TOKEN_ENV = "OURA_PERSONAL_ACCESS_TOKEN"

mcp = _Server("oura")


def _token() -> str:
    token = os.environ.get(TOKEN_ENV, "").strip()
    if not token:
        raise RuntimeError(
            f"Missing {TOKEN_ENV}. Create a Personal Access Token at "
            "https://cloud.ouraring.com/personal-access-tokens and set it as an "
            "environment variable for this server."
        )
    return token


def _default_range(start_date: str | None, end_date: str | None) -> tuple[str, str]:
    """Default to the last 7 days when a range isn't supplied."""
    end = end_date or date.today().isoformat()
    start = start_date or (date.fromisoformat(end) - timedelta(days=6)).isoformat()
    return start, end


def _get(path: str, params: dict[str, Any] | None = None) -> str:
    """Call an Oura API v2 endpoint and return the JSON response as text.

    Follows Oura's cursor pagination automatically, concatenating pages into a
    single `data` list so callers don't have to page manually.
    """
    headers = {"Authorization": f"Bearer {_token()}"}
    params = dict(params or {})
    url = f"{API_BASE}/{path.lstrip('/')}"

    aggregated: list[Any] | None = None
    single: dict[str, Any] | None = None

    with httpx.Client(timeout=30.0) as client:
        while True:
            resp = client.get(url, headers=headers, params=params)
            if resp.status_code == 401:
                raise RuntimeError(
                    "Oura API returned 401 Unauthorized — the Personal Access "
                    "Token is missing, invalid, or expired."
                )
            if resp.status_code == 429:
                raise RuntimeError(
                    "Oura API rate limit hit (429). Wait a moment and retry with "
                    "a narrower date range."
                )
            resp.raise_for_status()
            payload = resp.json()

            # Collection endpoints return {"data": [...], "next_token": ...}.
            if isinstance(payload, dict) and "data" in payload:
                if aggregated is None:
                    aggregated = []
                aggregated.extend(payload.get("data", []))
                next_token = payload.get("next_token")
                if next_token:
                    params["next_token"] = next_token
                    continue
                break

            # Single-object endpoints (e.g. personal_info) return a bare object.
            single = payload
            break

    if aggregated is not None:
        return json.dumps({"data": aggregated, "count": len(aggregated)}, indent=2)
    return json.dumps(single, indent=2)


# --- Profile -----------------------------------------------------------------


@mcp.tool()
def get_personal_info() -> str:
    """Get the user's Oura profile: age, weight, height, biological sex, email."""
    return _get("personal_info")


# --- Daily summaries ----------------------------------------------------------


@mcp.tool()
def get_daily_sleep(start_date: str | None = None, end_date: str | None = None) -> str:
    """Daily sleep scores and contributors (efficiency, latency, REM, deep, etc.).

    Dates are ISO format (YYYY-MM-DD). Defaults to the last 7 days if omitted.
    """
    start, end = _default_range(start_date, end_date)
    return _get("daily_sleep", {"start_date": start, "end_date": end})


@mcp.tool()
def get_daily_readiness(start_date: str | None = None, end_date: str | None = None) -> str:
    """Daily readiness scores and contributors (HRV balance, resting HR, temp, etc.).

    Dates are ISO format (YYYY-MM-DD). Defaults to the last 7 days if omitted.
    """
    start, end = _default_range(start_date, end_date)
    return _get("daily_readiness", {"start_date": start, "end_date": end})


@mcp.tool()
def get_daily_activity(start_date: str | None = None, end_date: str | None = None) -> str:
    """Daily activity: steps, active/total calories, MET minutes, activity score.

    Dates are ISO format (YYYY-MM-DD). Defaults to the last 7 days if omitted.
    """
    start, end = _default_range(start_date, end_date)
    return _get("daily_activity", {"start_date": start, "end_date": end})


@mcp.tool()
def get_daily_stress(start_date: str | None = None, end_date: str | None = None) -> str:
    """Daily stress: high-stress and recovery-time seconds, and day summary.

    Dates are ISO format (YYYY-MM-DD). Defaults to the last 7 days if omitted.
    """
    start, end = _default_range(start_date, end_date)
    return _get("daily_stress", {"start_date": start, "end_date": end})


@mcp.tool()
def get_daily_spo2(start_date: str | None = None, end_date: str | None = None) -> str:
    """Daily blood-oxygen (SpO2) averages measured during sleep.

    Dates are ISO format (YYYY-MM-DD). Defaults to the last 7 days if omitted.
    """
    start, end = _default_range(start_date, end_date)
    return _get("daily_spo2", {"start_date": start, "end_date": end})


@mcp.tool()
def get_daily_resilience(start_date: str | None = None, end_date: str | None = None) -> str:
    """Daily resilience level and contributors (sleep recovery, daytime recovery).

    Dates are ISO format (YYYY-MM-DD). Defaults to the last 7 days if omitted.
    """
    start, end = _default_range(start_date, end_date)
    return _get("daily_resilience", {"start_date": start, "end_date": end})


# --- Detailed / event data ----------------------------------------------------


@mcp.tool()
def get_sleep_periods(start_date: str | None = None, end_date: str | None = None) -> str:
    """Detailed per-sleep-period data: stages, HR/HRV time series, timing, phases.

    This is richer than get_daily_sleep and can include multiple periods per day
    (e.g. naps). Dates are ISO format (YYYY-MM-DD). Defaults to the last 7 days.
    """
    start, end = _default_range(start_date, end_date)
    return _get("sleep", {"start_date": start, "end_date": end})


@mcp.tool()
def get_workouts(start_date: str | None = None, end_date: str | None = None) -> str:
    """Logged and auto-detected workouts: activity type, intensity, calories, timing.

    Dates are ISO format (YYYY-MM-DD). Defaults to the last 7 days if omitted.
    """
    start, end = _default_range(start_date, end_date)
    return _get("workout", {"start_date": start, "end_date": end})


@mcp.tool()
def get_sessions(start_date: str | None = None, end_date: str | None = None) -> str:
    """Guided/unguided moment sessions (breathing, meditation, rest, naps).

    Dates are ISO format (YYYY-MM-DD). Defaults to the last 7 days if omitted.
    """
    start, end = _default_range(start_date, end_date)
    return _get("session", {"start_date": start, "end_date": end})


@mcp.tool()
def get_heart_rate(start_datetime: str | None = None, end_datetime: str | None = None) -> str:
    """Time-series heart rate samples with bpm and source (awake/rest/sleep/workout).

    Datetimes are ISO 8601 (e.g. 2026-08-06T00:00:00+00:00). Note this endpoint
    uses datetime, not date. Defaults to the last 24 hours if omitted.
    """
    if not end_datetime:
        end_datetime = date.today().isoformat() + "T23:59:59+00:00"
    if not start_datetime:
        start_datetime = (date.today() - timedelta(days=1)).isoformat() + "T00:00:00+00:00"
    return _get("heartrate", {"start_datetime": start_datetime, "end_datetime": end_datetime})


# --- Escape hatch -------------------------------------------------------------


@mcp.tool()
def oura_get(path: str, start_date: str | None = None, end_date: str | None = None) -> str:
    """Call any Oura API v2 usercollection endpoint by path (escape hatch).

    Use for endpoints without a dedicated tool, e.g. "daily_cardiovascular_age",
    "vO2_max", "sleep_time", "rest_mode_period", "ring_configuration",
    "enhanced_tag". `path` is the segment after /v2/usercollection/.
    start_date/end_date (YYYY-MM-DD) are added when provided.
    """
    params: dict[str, Any] = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    return _get(path, params or None)


if __name__ == "__main__":
    mcp.run()
