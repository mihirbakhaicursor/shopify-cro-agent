# Pre-Audit — Page Priority Map

**Goal:** Before reviewing any page for UX or technical issues, identify which pages are actually worth fixing. A broken ATC button on a page getting 50 sessions/month is a P2. The same bug on a page getting 8,000 sessions/month is a P0.

**Runs:** After Audit 1 (Analytics Health), before Audit 2 (Heuristic Review).

**Requires:** Shopify MCP (minimum). Windsor/GA4 MCP improves accuracy. Meta/Google MCP shows which pages receive paid traffic.

**Output:** A ranked Page Priority Stack that every subsequent audit uses to weight findings.

---

## Step 1 — Pull top pages by session volume

Using Shopify MCP, pull the top 20 pages by sessions for the last 30 days:

```
ShopifyQL:
SELECT page_path, sessions, bounce_rate
FROM sessions
ORDER BY sessions DESC
LIMIT 20
DATE RANGE: last 30 days
```

If GA4 is connected via Windsor, cross-reference to confirm and add bounce rate and avg session duration per page.

For each page, classify:
- **Type:** homepage / collection (PLP) / product (PDP) / cart / checkout / other
- **Sessions:** raw number
- **% of total sessions:** sessions / total site sessions

---

## Step 2 — Pull top pages by revenue contribution

Using Shopify MCP, identify which product pages and collections are driving the most orders:

```
ShopifyQL:
SELECT landing_page, orders, total_sales
FROM orders
GROUP BY landing_page
ORDER BY total_sales DESC
LIMIT 20
DATE RANGE: last 30 days
```

For each page, calculate:
- **Revenue/session:** total_sales / sessions (cross-reference with Step 1)
- **Conversion rate:** orders / sessions

Revenue/session is the most important signal — it captures both traffic volume and conversion quality.

---

## Step 3 — Map paid traffic to landing pages

If Windsor, Meta Ads, or Google Ads MCP is connected:

Pull destination URLs for all active campaigns with > ₹500 / $10 spend in the last 30 days.

For each landing page receiving paid traffic:
- Record: ad platform, campaign name, spend (last 30 days), destination URL
- Note: **paid traffic pages are always high priority** — every ₹ of wasted traffic on a low-converting page is a directly recoverable cost

If no ads MCP is connected: skip this step, note the gap, proceed with organic traffic data only.

---

## Step 4 — Build the Page Priority Stack

Combine Steps 1–3 into a ranked table. Score each page:

```
Page Score = (sessions_rank × 0.4) + (revenue_rank × 0.4) + (paid_traffic × 0.2)
```

Where:
- `sessions_rank` = 1.0 for top session page, scaled down proportionally
- `revenue_rank` = 1.0 for top revenue page, scaled down proportionally  
- `paid_traffic` = 1.0 if page receives paid traffic, 0.5 if organic only, 0 if neither

Output a ranked table like this:

```
PAGE PRIORITY STACK — [Store Name] — [Date]

Tier 1 (Must audit — high traffic + high revenue or paid traffic)
┌─────────────────────────────────┬──────────┬──────────┬────────────┬───────────────┐
│ Page                            │ Sessions │ Revenue  │ Rev/Session│ Paid Traffic? │
├─────────────────────────────────┼──────────┼──────────┼────────────┼───────────────┤
│ /products/best-seller           │ 4,200    │ ₹1.8L    │ ₹42.8      │ Yes — Meta    │
│ /collections/gifts              │ 3,100    │ ₹0.9L    │ ₹29.0      │ Yes — Google  │
│ / (homepage)                    │ 8,400    │ ₹0.4L    │ ₹4.8       │ Yes — both    │
└─────────────────────────────────┴──────────┴──────────┴────────────┴───────────────┘

Tier 2 (Audit if time allows — decent traffic, lower revenue or organic only)
│ /products/new-arrival           │ 1,200    │ ₹0.3L    │ ₹25.0      │ No            │
│ /collections/all                │ 2,800    │ ₹0.1L    │ ₹3.6       │ No            │

Tier 3 (Skip unless specifically flagged — low traffic, low revenue)
│ /pages/about                    │ 340      │ ₹0       │ ₹0         │ No            │
```

---

## Step 5 — Note the CVR gap pages

From the page data, flag any page where:
- Sessions are **high** (top 5) but revenue/session is **low** (bottom 5)

These are your highest-leverage pages — lots of people are landing there but not converting. A CVR improvement on these pages moves the needle more than any other single change.

```
CVR GAP PAGES (high traffic, low revenue/session):
- /collections/all — 2,800 sessions, ₹3.6/session vs ₹29 site average → 8× below average
- / (homepage) — 8,400 sessions, ₹4.8/session → likely a navigation/funnel issue, not a product issue
```

---

## Output

Write the Page Priority Stack to your audit notes. Reference it in every subsequent audit:

- **Audit 2 (Heuristic):** Review Tier 1 pages first and in full. Review Tier 2 pages if time allows. Skip Tier 3 unless the user flags them.
- **Audit 3 (Technical):** Run PageSpeed and check for JS errors on Tier 1 pages first.
- **Audit 4 (Behavioural):** Pull Clarity heatmaps and scroll data for Tier 1 pages only — don't waste time on low-traffic pages.
- **Phase 5 (Scoring):** PXL question 4 ("high traffic page?") is answered YES for Tier 1, NO for Tier 2+. A finding on a Tier 1 page with paid traffic gets +1 on PXL automatically.

The Page Priority Stack does not create findings. It is the lens through which findings are weighted.
