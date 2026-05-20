#!/usr/bin/env python3
"""
Shopify CRO Agent — Issue Tracker + Dashboard Generator
────────────────────────────────────────────────────────
This script reads issue_statuses.json (written by Claude during audits)
and generates a visual HTML dashboard showing open/fixed issues,
priorities, and remediation status.

Run after each audit session:
    python3 cro_agent.py

Or schedule for weekly scans:
    0 9 * * 1 cd /path/to/shopify-cro-agent && python3 cro_agent.py
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT       = Path(__file__).parent
DATA_DIR   = ROOT / "data"
OUTPUT_DIR = ROOT / "output"
CONFIG_F   = ROOT / "store_config.json"
ISSUES_F   = DATA_DIR / "issue_statuses.json"
DASH_OUT   = OUTPUT_DIR / "cro_dashboard.html"

OUTPUT_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# ── Load config ────────────────────────────────────────────────────────────────

def load_config():
    if not CONFIG_F.exists():
        print("[warn] store_config.json not found — using defaults. Copy store_config.example.json to get started.")
        return {"store": {"name": "Your Store", "url": "#", "currency": "USD"}}
    with open(CONFIG_F) as f:
        return json.load(f)

# ── Load issues ────────────────────────────────────────────────────────────────

def load_issues():
    if not ISSUES_F.exists():
        return {}
    with open(ISSUES_F) as f:
        raw = json.load(f)
    # Skip metadata keys (string values) — only keep issue entries (dict values)
    return {k: v for k, v in raw.items() if isinstance(v, dict)}

# ── Dashboard generator ────────────────────────────────────────────────────────

def generate_dashboard(config, issues):
    store_name = config.get("store", {}).get("name", "Your Store")
    store_url  = config.get("store", {}).get("url", "#")
    now        = datetime.now().strftime("%Y-%m-%d %H:%M")

    open_issues   = {k: v for k, v in issues.items() if v.get("status") == "open"}
    fixed_issues  = {k: v for k, v in issues.items() if v.get("status") == "fixed"}

    def issue_rows(issue_dict, show_fix=False):
        if not issue_dict:
            return "<tr><td colspan='4' style='color:#888;text-align:center;padding:20px'>None</td></tr>"
        rows = []
        for iid, data in sorted(issue_dict.items(), key=lambda x: x[1].get("first_detected", "")):
            detected = data.get("first_detected", "—")
            last     = data.get("last_seen", "—")
            fixed    = data.get("fixed_date", "—")
            label    = iid.replace("_", " ").title()
            status   = data.get("status", "open")
            badge    = (
                "<span style='background:#22c55e;color:#fff;border-radius:4px;padding:2px 8px;font-size:11px'>FIXED</span>"
                if status == "fixed" else
                "<span style='background:#ef4444;color:#fff;border-radius:4px;padding:2px 8px;font-size:11px'>OPEN</span>"
            )
            if show_fix:
                rows.append(f"<tr><td>{badge}</td><td style='font-family:monospace;font-size:12px'>{iid}</td><td>{label}</td><td>{detected}</td><td>{fixed}</td></tr>")
            else:
                rows.append(f"<tr><td>{badge}</td><td style='font-family:monospace;font-size:12px'>{iid}</td><td>{label}</td><td>{detected}</td><td>{last}</td></tr>")
        return "\n".join(rows)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CRO Dashboard — {store_name}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f172a; color: #e2e8f0; padding: 24px; }}
  .header {{ margin-bottom: 32px; }}
  .header h1 {{ font-size: 24px; font-weight: 700; color: #f8fafc; }}
  .header p {{ color: #94a3b8; font-size: 14px; margin-top: 4px; }}
  .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 16px; margin-bottom: 32px; }}
  .stat {{ background: #1e293b; border-radius: 10px; padding: 20px; }}
  .stat .val {{ font-size: 32px; font-weight: 700; color: #f8fafc; }}
  .stat .lbl {{ font-size: 12px; color: #94a3b8; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.05em; }}
  .stat.red .val {{ color: #f87171; }}
  .stat.green .val {{ color: #4ade80; }}
  .section {{ background: #1e293b; border-radius: 10px; padding: 24px; margin-bottom: 24px; }}
  .section h2 {{ font-size: 16px; font-weight: 600; color: #f8fafc; margin-bottom: 16px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th {{ text-align: left; color: #64748b; padding: 8px 12px; border-bottom: 1px solid #334155; font-weight: 500; text-transform: uppercase; font-size: 11px; letter-spacing: 0.05em; }}
  td {{ padding: 10px 12px; border-bottom: 1px solid #1e293b; color: #cbd5e1; vertical-align: middle; }}
  tr:last-child td {{ border-bottom: none; }}
  tr:hover td {{ background: #263045; }}
  .footer {{ color: #475569; font-size: 12px; margin-top: 32px; text-align: center; }}
  a {{ color: #60a5fa; text-decoration: none; }}
</style>
</head>
<body>

<div class="header">
  <h1>CRO Dashboard — {store_name}</h1>
  <p><a href="{store_url}" target="_blank">{store_url}</a> · Last updated {now}</p>
</div>

<div class="stats">
  <div class="stat red">
    <div class="val">{len(open_issues)}</div>
    <div class="lbl">Open Issues</div>
  </div>
  <div class="stat green">
    <div class="val">{len(fixed_issues)}</div>
    <div class="lbl">Fixed</div>
  </div>
  <div class="stat">
    <div class="val">{len(issues)}</div>
    <div class="lbl">Total Found</div>
  </div>
  <div class="stat">
    <div class="val">{round(len(fixed_issues) / max(len(issues), 1) * 100)}%</div>
    <div class="lbl">Resolution Rate</div>
  </div>
</div>

<div class="section">
  <h2>🔴 Open Issues ({len(open_issues)})</h2>
  <table>
    <tr>
      <th>Status</th><th>ID</th><th>Issue</th><th>First Detected</th><th>Last Seen</th>
    </tr>
    {issue_rows(open_issues, show_fix=False)}
  </table>
</div>

<div class="section">
  <h2>✅ Fixed Issues ({len(fixed_issues)})</h2>
  <table>
    <tr>
      <th>Status</th><th>ID</th><th>Issue</th><th>First Detected</th><th>Fixed Date</th>
    </tr>
    {issue_rows(fixed_issues, show_fix=True)}
  </table>
</div>

<div class="footer">
  Generated by <a href="https://github.com/mihirbakhaicursor/shopify-cro-agent">shopify-cro-agent</a> · {now}
</div>

</body>
</html>"""

    DASH_OUT.write_text(html)
    print(f"[ok] Dashboard written to {DASH_OUT}")
    return DASH_OUT


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    config = load_config()
    issues = load_issues()

    if not issues:
        print("[info] No issues found in issue_statuses.json. Run a scan first.")
        print("[info] In Claude Code: 'Run a first CRO scan on my store'")
        sys.exit(0)

    open_count  = sum(1 for v in issues.values() if v.get("status") == "open")
    fixed_count = sum(1 for v in issues.values() if v.get("status") == "fixed")

    print(f"[info] {len(issues)} total issues: {open_count} open, {fixed_count} fixed")

    out = generate_dashboard(config, issues)
    print(f"[info] Open in browser: open {out}")


if __name__ == "__main__":
    main()
