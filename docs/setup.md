# Setup Guide

This guide walks through connecting the tools you need before running your first CRO scan.

---

## Required: Claude Code

You need [Claude Code](https://claude.ai/code) — the CLI version of Claude that can use tools and access your store data.

Install: follow the instructions at https://claude.ai/code

Once installed, open a terminal in this project directory:
```bash
cd shopify-cro-agent
claude .
```

---

## Required: Shopify MCP

The Shopify MCP gives Claude direct access to your store's orders, products, sessions, abandoned checkouts, and customer data via Shopify's API.

**Setup:**
1. Install the Shopify MCP: https://github.com/shopify/dev-mcp
2. Authenticate with your Shopify store admin credentials
3. Verify: ask Claude `"List my last 5 orders"` — if it returns real orders, the MCP is working

**What it unlocks:**
- Audits 1, 2, 3, 6 (and parts of 4, 5)
- All ShopifyQL queries (sessions, orders, funnel, products)
- Abandoned checkout data
- Customer lifetime value and repeat purchase analysis

---

## Strongly recommended: Microsoft Clarity MCP

Clarity is a free heatmap and session recording tool from Microsoft. It's required for Audit 4 (behavioural) — the audit that shows you what visitors are actually doing.

**If you don't have Clarity installed on your store:**
1. Go to https://clarity.microsoft.com
2. Create a free account
3. Add the Clarity tracking script to your Shopify theme:
   - Shopify Admin → Online Store → Themes → Edit Code
   - Add the Clarity script in `theme.liquid` before `</head>`
4. Wait 24–48 hours for data to accumulate before running Audit 4

**Connecting the MCP:**
1. Install the Clarity MCP (link in Clarity dashboard under "Integrations")
2. Authenticate with your Clarity account

**What it unlocks:**
- Scroll depth per page
- Click heatmaps (rage clicks, dead clicks)
- Session recordings
- Device-level behaviour differences

**Note:** If Clarity is newly installed, run Audits 1–3 and 5–6 first, then circle back to Audit 4 once you have 2+ weeks of data.

---

## Optional: Windsor.ai MCP (Meta + Google + GA4)

Windsor aggregates data from Meta Ads, Google Ads, and Google Analytics 4 into a single MCP connection.

**Setup:**
1. Create a Windsor.ai account at https://windsor.ai
2. Connect your data sources in the Windsor dashboard:
   - Meta Ads → connect your ad account
   - Google Ads → connect your ad account
   - Google Analytics 4 → connect your property
3. Install the Windsor MCP and authenticate

**What it unlocks:**
- Audit 1: GA4 session data, conversion tracking
- Audit 5: Meta and Google campaign performance, ROAS by campaign

**Alternative:** If you don't want to use Windsor, you can connect the Meta Ads MCP and Google Ads MCP directly instead.

---

## Optional: Meta Ads MCP

Direct connection to Meta Ads (Facebook/Instagram). Useful if you don't use Windsor.

**Setup:**
1. Install the Meta Ads MCP
2. Authenticate with your Meta Business Manager account
3. Grant access to the relevant ad account(s)

---

## What happens without each MCP

| Missing MCP | What gets skipped |
|-------------|------------------|
| Shopify MCP | All audits — cannot proceed without this |
| Clarity MCP | Audit 4 skipped entirely. Audits 2+3 still run (heuristic + technical). You lose scroll depth, heatmaps, rage click data. |
| Windsor/Meta MCP | Audit 5 (paid traffic) skipped. You can still audit your organic store performance. |

The agent will tell you exactly which audits are available based on what's connected, and what you'd gain from connecting the missing tools.

---

## Filling in store_config.json

Copy the example and fill in what you know:

```bash
cp store_config.example.json store_config.json
```

**You don't need to fill in everything.** The agent will pull most metrics live from your MCPs. But these fields help it give better-calibrated estimates:

- `store.url` — your live store URL
- `store.currency` — affects all ₹/$ calculations
- `store.category` — helps interpret conversion rate benchmarks
- `baseline_metrics.monthly_sessions` — needed for A/B test sample size calculations
- `baseline_metrics.overall_cvr_pct` — needed for MDE calculations
- `tools.checkout` — critical for Audit 3 (checkout-specific issues vary by tool)

---

## Verifying your setup

Before starting the scan, run a quick connection check:

```
"Check which MCPs are connected and what's available for the CRO scan"
```

The agent will tell you:
- Which MCPs are live
- Which audits can run
- What's missing and what it would unlock

Once you're satisfied, start with:
```
"Run a first CRO scan on my store"
```
