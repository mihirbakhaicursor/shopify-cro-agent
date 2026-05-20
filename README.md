# Shopify CRO Agent

A Claude-powered conversion rate optimisation agent for Shopify stores. Run a full 6-audit CRO scan directly in your terminal — using Claude Code with your live store data.

**What a first scan actually found on a real store:**

- 75% of mobile visitors couldn't see the Add to Cart button at all
- ₹6,868/month in Google Ads spend on a campaign with 0 conversions
- ₹3.94L/month in abandoned checkouts with zero recovery emails
- The Meta Pixel had been firing 0 purchase events for 6+ weeks — every ad rupee optimising toward nothing
- A checkout OTP wall estimated to be abandoning ₹28L/month — invisible to Shopify's analytics

That store was [Adorn Silver](https://www.adornsilver.co) — ₹3.37 Cr revenue, 23× growth in 2 years. They didn't know about most of these. Neither do most stores.

---

## What this agent does

It runs **6 sequential audits** against your Shopify store, then scores every finding with the [PXL framework](https://cxl.com/blog/pxl-prioritization-framework/) (CXL/Speero) and produces a prioritised action plan.

| Audit | What it covers |
|-------|---------------|
| 01 — Analytics Health | GA4/pixel setup, tracking gaps, attribution blind spots |
| 02 — Heuristic | LIFT model review of homepage, PLP, PDP, checkout |
| 03 — Technical | PageSpeed, Core Web Vitals, script bloat, checkout JS errors |
| 04 — Behavioural | Clarity heatmaps, scroll depth, rage clicks, session replays |
| 05 — Paid Traffic | Ad spend efficiency, landing page mismatch, ROAS by campaign |
| 06 — Revenue & AOV | Abandonment recovery, upsell gaps, retention leaks, AOV audit |

**Phase 5** then scores every finding (10 binary PXL questions), classifies them into tiers, and outputs:
- Quick wins to ship this week
- An A/B test roadmap with sample size calculations
- A developer briefing doc

---

## What you get at the end

```
output/
├── cro_dashboard.html      ← Visual issue tracker (open in browser)
└── sprint1_briefing.md     ← Dev-ready brief: issue, hypothesis, exact fix steps
```

Plus a live `data/issue_statuses.json` that tracks every finding across future scans.

---

## Prerequisites

| Tool | Required | What it's used for |
|------|----------|-------------------|
| [Claude Code](https://claude.ai/code) | ✅ Required | The AI that runs the audits |
| [Shopify MCP](https://github.com/shopify/dev-mcp) | ✅ Required | Live store data: orders, products, checkouts, sessions |
| [Microsoft Clarity MCP](https://clarity.microsoft.com) | ⭐ Strongly recommended | Heatmaps, scroll depth, rage clicks, session replays |
| [Windsor.ai MCP](https://windsor.ai) | Optional | Meta Ads, Google Ads, GA4 data |
| [Meta Ads MCP](https://developers.facebook.com/docs/marketing-api/) | Optional | Detailed Meta campaign analysis |

The agent gracefully skips audits for any MCP that isn't connected and tells you what you're missing.

---

## Quickstart

```bash
# 1. Clone the repo
git clone https://github.com/mihirbakhaicursor/shopify-cro-agent
cd shopify-cro-agent

# 2. Copy and fill in your store config
cp store_config.example.json store_config.json
# Edit store_config.json with your store URL, currency, and goals

# 3. Open in Claude Code
claude .

# 4. Tell Claude to start the scan
"Run a first CRO scan on my store"

# 5. Follow the guided audit sequence
# Each audit takes 15–30 minutes. Total: ~2–3 hours for all 6 + scoring.
```

**Time to first findings:** ~20 minutes (Audit 1 + 2 alone surface most critical issues).

---

## First scan experience

The agent is designed for a **discovery audit** — you're not monitoring a live dashboard, you're running a structured investigation for the first time. The docs walk you through each audit with:

- What evidence to look for
- What questions to answer
- How to interpret what you find
- What "good" vs "broken" looks like

Start here: **[docs/first-scan.md](docs/first-scan.md)**

---

## Real results from Adorn Silver

Adorn Silver (D2C silver gifting, India) ran this full audit pipeline in May 2026. Results:

**Critical bugs found:**
- Meta Pixel: 0 purchase events firing for 6+ weeks → Audit 1
- Shopflo payment tracking broken → Audit 3
- Google Ads campaign with ₹6,868 spend, 0 conversions → Audit 5

**UX issues found:**
- ATC button below fold on 75% of mobile devices → Audit 2 + 4
- Hero section: 0 CTAs on a page receiving 100% of paid traffic → Audit 2
- Checkout OTP wall causing mass abandonment → Audit 3

**Revenue leakage found:**
- ₹3.94L/month abandoned checkouts, zero recovery emails → Audit 6
- Estimated ₹28L/month in Shopflo-invisible abandonments → Audit 6
- No post-purchase upsell on any product → Audit 6

**Quick wins (shipped without A/B testing):** 20 items
**A/B tests queued:** 3 (limited by traffic)
**Total estimated monthly revenue impact:** ₹3.1L–₹4.7L

Full case study: [docs/case-study-adorn.md](docs/case-study-adorn.md)

---

## How the PXL scoring works

Every finding gets scored on 10 binary questions (yes = 1, no = 0):

1. Is the change above the fold?
2. Is it backed by quantitative data?
3. Is it backed by qualitative/behavioural data?
4. Does it affect a page with high traffic?
5. Is it a bug fix? (ship directly, no test needed)
6. Does it directly affect the primary conversion action?
7. Is the change noticeable within 5 seconds?

Score ≥ 7 → A/B test, high priority  
Score 5–6 → A/B test, next sprint  
Low effort + low risk → Ship directly (no test)  
Score < 5 + low traffic → Fix based on heuristics only  
Score < 4 + complex → Defer

The agent calculates required sample sizes and checks if your traffic can reach statistical significance within 4 weeks before recommending an A/B test.

---

## Project structure

```
shopify-cro-agent/
├── README.md                    ← You are here
├── CLAUDE.md                    ← Agent instructions (the brain)
├── store_config.example.json    ← Copy this → store_config.json
├── cro_agent.py                 ← Issue tracker + dashboard generator
├── audits/
│   ├── 01_analytics.md          ← Audit 1 spec
│   ├── 02_heuristic.md          ← Audit 2 spec
│   ├── 03_technical.md          ← Audit 3 spec
│   ├── 04_behavioural.md        ← Audit 4 spec
│   ├── 05_paid_traffic.md       ← Audit 5 spec
│   ├── 06_revenue_aov.md        ← Audit 6 spec
│   └── 07_phase5_scoring.md     ← Scoring + prioritisation spec
├── data/
│   └── issue_statuses.json      ← Created on first scan
├── output/                      ← Generated output (gitignored)
│   ├── cro_dashboard.html
│   └── sprint1_briefing.md
└── docs/
    ├── first-scan.md            ← Start here for your first run
    ├── setup.md                 ← MCP setup guide
    ├── interpreting-findings.md ← How to read and act on results
    └── case-study-adorn.md      ← Full Adorn Silver case study
```

---

## Contributing

The audit specs in `/audits/` are markdown files — you can extend them, add new checks, or adapt them for different store types (fashion, food, B2B).

If you find something in your scan that isn't in the audit specs, open a PR with the finding pattern added to the relevant audit file.

---

## License

MIT. Use it, fork it, ship it.
