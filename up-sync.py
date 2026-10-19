#!/usr/bin/env python3
"""
up-sync — pull live balances from the Up Banking API (read-only).

No more screenshots. Reads your Up Personal Access Token from the UP_TOKEN
environment variable and prints every account + saver balance.

SETUP (one-time, done in your Claude Code environment settings, NOT in chat):
  1. Network access  → allow the domain  api.up.com.au
  2. Network secrets → store your Up token as an env var named  UP_TOKEN
     (generate the token from https://developer.up.com.au/#getting-started)

The Up public API is READ-ONLY — this script can see balances and
transactions, it cannot move money. Revoke the token anytime in the Up app.

USAGE:
  python3 up-sync.py              # pretty summary of all accounts + savers
  python3 up-sync.py --json       # structured JSON (for the dashboards)
  python3 up-sync.py --ping       # just check the token works
  python3 up-sync.py --tx 20      # also list the 20 most recent transactions
"""

import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from urllib.parse import urlencode

API = "https://api.up.com.au/api/v1"
CA_BUNDLE = "/root/.ccr/ca-bundle.crt"  # proxy CA in this cloud environment


def _ssl_context():
    ctx = ssl.create_default_context()
    # Trust the environment's egress-proxy CA on top of the system store.
    if os.path.exists(CA_BUNDLE):
        try:
            ctx.load_verify_locations(cafile=CA_BUNDLE)
        except Exception:
            pass
    return ctx


def _opener():
    # urllib reads HTTPS_PROXY/http_proxy from the environment automatically;
    # being explicit keeps it robust if those names change.
    handlers = [urllib.request.HTTPSHandler(context=_ssl_context())]
    proxies = urllib.request.getproxies()
    if proxies:
        handlers.append(urllib.request.ProxyHandler(proxies))
    return urllib.request.build_opener(*handlers)


def _get(path_or_url, token):
    """GET an API path (or a full pagination URL) and return parsed JSON."""
    url = path_or_url if path_or_url.startswith("http") else API + path_or_url
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    })
    with _opener().open(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_accounts(token):
    """Return all accounts, following pagination."""
    out, url = [], "/accounts?" + urlencode({"page[size]": 100})
    while url:
        page = _get(url, token)
        out.extend(page.get("data", []))
        url = (page.get("links") or {}).get("next")
    return out


def fetch_transactions(token, limit):
    page = _get("/transactions?" + urlencode({"page[size]": min(limit, 100)}), token)
    return page.get("data", [])[:limit]


def _money(attrs):
    bal = attrs.get("balance", {})
    try:
        return float(bal.get("value", "0"))
    except (TypeError, ValueError):
        return 0.0


def _die_setup(msg):
    print(f"\n⚠️  {msg}\n", file=sys.stderr)
    print("Checklist (set in your Claude Code environment, not in chat):", file=sys.stderr)
    print("  • Network access  → allow  api.up.com.au", file=sys.stderr)
    print("  • Network secrets → env var  UP_TOKEN  = your Up token", file=sys.stderr)
    print("    token from https://developer.up.com.au/#getting-started", file=sys.stderr)
    sys.exit(1)


def _call(fn, *a):
    """Run an API call, turning the common failures into clear guidance."""
    try:
        return fn(*a)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            _die_setup("Up rejected the token (401). It's missing, wrong, or revoked — "
                       "regenerate it in the Up app and update the UP_TOKEN secret.")
        _die_setup(f"Up API returned HTTP {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        _die_setup(f"Couldn't reach api.up.com.au ({e.reason}). The environment's "
                   "network policy probably still blocks it — allow the domain.")
    except Exception as e:  # noqa: BLE001
        _die_setup(f"Unexpected error: {e}")


def main():
    ap = argparse.ArgumentParser(description="Pull live Up balances (read-only).")
    ap.add_argument("--json", action="store_true", help="emit structured JSON")
    ap.add_argument("--ping", action="store_true", help="just verify the token")
    ap.add_argument("--tx", type=int, metavar="N", default=0,
                    help="also list the N most recent transactions")
    args = ap.parse_args()

    token = os.environ.get("UP_TOKEN", "").strip()
    if not token:
        _die_setup("UP_TOKEN is not set in the environment.")

    if args.ping:
        _call(_get, "/util/ping", token)
        print("✅ Token works — Up API reachable.")
        return

    accounts = _call(fetch_accounts, token)

    # Split savers from the transactional (Spending) account.
    savers = [a for a in accounts if a["attributes"].get("accountType") == "SAVER"]
    txnl = [a for a in accounts if a["attributes"].get("accountType") != "SAVER"]
    savers.sort(key=lambda a: _money(a["attributes"]), reverse=True)

    if args.json:
        payload = {
            "accounts": [
                {
                    "id": a["id"],
                    "name": a["attributes"].get("displayName"),
                    "type": a["attributes"].get("accountType"),
                    "balance": _money(a["attributes"]),
                    "currency": a["attributes"].get("balance", {}).get("currencyCode"),
                }
                for a in txnl + savers
            ],
        }
        payload["total"] = round(sum(x["balance"] for x in payload["accounts"]), 2)
        if args.tx:
            txs = _call(fetch_transactions, token, args.tx)
            payload["transactions"] = [
                {
                    "date": t["attributes"].get("createdAt"),
                    "description": t["attributes"].get("description"),
                    "amount": t["attributes"].get("amount", {}).get("value"),
                    "status": t["attributes"].get("status"),
                }
                for t in txs
            ]
        print(json.dumps(payload, indent=2))
        return

    # Pretty summary
    total = 0.0
    print("\n  UP — live balances\n  " + "─" * 34)
    for a in txnl:
        bal = _money(a["attributes"])
        total += bal
        print(f"  {a['attributes'].get('displayName',''):<24}${bal:>10,.2f}")
    if savers:
        print("  " + "·" * 34)
        for a in savers:
            bal = _money(a["attributes"])
            total += bal
            print(f"  {a['attributes'].get('displayName',''):<24}${bal:>10,.2f}")
    print("  " + "─" * 34)
    print(f"  {'TOTAL':<24}${total:>10,.2f}\n")

    if args.tx:
        txs = _call(fetch_transactions, token, args.tx)
        print(f"  Last {len(txs)} transactions\n  " + "─" * 34)
        for t in txs:
            at = t["attributes"]
            amt = at.get("amount", {}).get("value", "")
            desc = (at.get("description") or "")[:26]
            print(f"  {desc:<28}{amt:>12}")
        print()


if __name__ == "__main__":
    main()
