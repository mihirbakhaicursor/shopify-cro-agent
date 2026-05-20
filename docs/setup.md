# Setup Guide

This guide walks through connecting the tools you need before running your first CRO scan.

**Time to complete:** 30–60 minutes depending on which tools you connect.

---

## Required: Claude Code

Install [Claude Code](https://claude.ai/code) — the CLI that runs the audits.

```bash
# Once installed, open this project directory
cd shopify-cro-agent
claude .
```

---

## Required: Shopify MCP

The Shopify MCP is the easiest to set up — one click from Shopify admin.

**Steps:**
1. In your Shopify Admin, go to **Settings → Apps and sales channels**
2. Install the [Shopify Dev MCP](https://github.com/shopify/dev-mcp) — follow the instructions there
3. Authenticate with your store credentials when prompted
4. Verify it's working — ask Claude: `"List my last 5 orders"`

**What it unlocks:** Orders, products, abandoned checkouts, session analytics, customer data, ShopifyQL queries — the backbone of all 6 audits.

> Without Shopify MCP the agent cannot run. Everything else is optional.

---

## Strongly Recommended: Microsoft Clarity MCP

Clarity is a free behavioural analytics tool (heatmaps, scroll depth, session recordings). Required for Audit 4.

### Step 1 — Install Clarity on your store (skip if already done)

1. Go to [clarity.microsoft.com](https://clarity.microsoft.com) → create a free account
2. Create a new project for your store
3. Copy your **Project ID** (shown in Settings → Overview)
4. Add the tracking script to your Shopify theme:
   - Shopify Admin → **Online Store → Themes → Edit Code**
   - Open `theme.liquid`
   - Paste the Clarity script tag just before `</head>`:
   ```html
   <script type="text/javascript">
     (function(c,l,a,r,i,t,y){
       c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
       t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
       y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
     })(window, document, "clarity", "script", "YOUR_PROJECT_ID");
   </script>
   ```
5. Replace `YOUR_PROJECT_ID` with your actual Project ID → Save

### Step 2 — Connect the Clarity MCP

1. In Clarity dashboard, go to **Settings → Integrations → MCP**
2. Copy the MCP configuration snippet
3. Add it to your Claude Code MCP config (`~/.claude/mcp_servers.json` or via `claude mcp add`)
4. Restart Claude Code and verify: ask Claude `"What's my Clarity project ID?"`

**Note:** Wait at least 48–72 hours after installing Clarity before running Audit 4. The agent will tell you if there's not enough data yet and suggest running the other audits first.

**What it unlocks:**
- Scroll depth per page (how far visitors actually get)
- Click heatmaps — dead clicks, rage clicks, ignored CTAs
- Session recordings
- Device-level behaviour differences (mobile vs desktop)
- JS error counts per page

---

## Optional: Windsor.ai MCP (Meta Ads + Google Ads + GA4)

Windsor aggregates Meta, Google, and GA4 data into one connection. Required for Audit 5 (paid traffic) and Audit 1 (analytics health).

### Step 1 — Create a Windsor account and connect sources

1. Go to [windsor.ai](https://windsor.ai) → sign up
2. In the Windsor dashboard, go to **Data Sources → Add Connector**
3. Connect each source you use:

   **Meta Ads:**
   - Select connector: `Facebook Ads`
   - Click Connect → authenticate with your Meta Business Manager
   - Select the ad account(s) you want to include
   - Connector name in Windsor will appear as `facebook`

   **Google Ads:**
   - Select connector: `Google Ads`
   - Click Connect → authenticate with the Google account that owns the ad account
   - Select your Google Ads customer ID

   **Google Analytics 4:**
   - Select connector: `Google Analytics 4`
   - Click Connect → authenticate → select your GA4 property

4. Wait 15–30 minutes for Windsor to sync initial data

### Step 2 — Get your Windsor API key

1. Windsor dashboard → **Account Settings → API Keys**
2. Generate a new API key → copy it

### Step 3 — Connect the Windsor MCP

Add to your MCP config:

```json
{
  "mcpServers": {
    "windsor": {
      "command": "npx",
      "args": ["-y", "@windsor-ai/mcp"],
      "env": {
        "WINDSOR_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

Or via CLI:
```bash
claude mcp add windsor -- npx -y @windsor-ai/mcp
# Then set WINDSOR_API_KEY in your environment
```

Verify: ask Claude `"What connectors are available in Windsor?"` — it should list `facebook`, `google_ads`, `google_analytics_4`.

**Known field gotchas:**
- Meta Ads conversions: use `actions` field filtered for `offsite_conversion.fb_pixel_purchase` — not `conversions` or `conversion_value` (those are often empty or wrong)
- Google Ads: use `cost`, `clicks`, `impressions`, `conversions` — the `conversions` field here is reliable
- GA4: use `sessions`, `users`, `bounce_rate`

**What it unlocks:**
- Audit 1: GA4 tracking gaps, pixel health, attribution discrepancies
- Audit 5: ROAS by campaign, dead campaigns, Meta vs Google spend efficiency

---

## Optional: Meta Ads MCP (direct, without Windsor)

Use this instead of Windsor if you only run Meta ads and don't need GA4/Google Ads data.

### Steps

1. Go to [Meta for Developers](https://developers.facebook.com) → create an app if you don't have one
2. Generate a **User Access Token** with these permissions:
   - `ads_read`
   - `ads_management`
   - `business_management`
3. Add to your MCP config:

```json
{
  "mcpServers": {
    "meta-ads": {
      "command": "npx",
      "args": ["-y", "@anthropic-samples/meta-ads-mcp"],
      "env": {
        "META_ACCESS_TOKEN": "your_token_here",
        "META_AD_ACCOUNT_ID": "act_123456789"
      }
    }
  }
}
```

4. Verify: ask Claude `"What's my Meta ad account spend this month?"`

---

## What happens without each MCP

| MCP | Status | Audits affected | What you lose |
|-----|--------|----------------|---------------|
| Shopify | **Required** | All | Cannot run any audit |
| Clarity | Strongly recommended | Audit 4 | Heatmaps, scroll depth, rage clicks, JS error data |
| Windsor / Meta | Optional | Audit 1 + 5 | Pixel health check, ROAS by campaign, dead spend detection |

The agent will tell you at the start which audits can run and what connecting the missing tools would unlock.

---

## store_config.json — you don't fill this in manually

When you run `"Run a first CRO scan on my store"`, Claude will ask you 5 questions and write the config file itself:

1. Store URL
2. Shopify domain (yourstore.myshopify.com)
3. Currency
4. What you sell + average order value
5. Rough monthly sessions and orders (ballpark is fine)

That's it. Everything else — exact CVR, session volumes, revenue by channel — gets pulled live from your MCPs during the audits and filled in as the scan runs.

If you want to pre-fill it manually (e.g. you're setting up for a client), copy the example:

```bash
cp store_config.example.json store_config.json
```

The file is gitignored — it never gets committed.

---

## Verifying your full setup

Before starting the scan, run:

```
"Check which MCPs are connected and what's available for the CRO scan"
```

The agent will confirm which audits can run. Once ready:

```
"Run a first CRO scan on my store"
```
