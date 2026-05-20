# Phase 5 — Hypothesis Scoring and Prioritisation

**Goal:** Score every confirmed finding from Audits 1–6 using the PXL framework. Produce a prioritised action plan: quick wins to ship this week, A/B tests to run this sprint, and a developer briefing document.

**Constraint:** Never let enthusiasm override a low PXL score. If an idea scores below 5, it waits. No exceptions.

---

## Step 1: Compile all confirmed findings

Pull every entry from `data/issue_statuses.json` with `"status": "open"`.

For each issue, you should have (from the audit that found it):
- Title
- Priority (P0/P1/P2)
- Evidence
- Hypothesis
- Estimated impact (₹ or %)
- Effort

If any are missing, go back to the relevant audit output and fill them in before scoring.

---

## Step 2: PXL scoring

Score each finding on these 7 binary questions (yes = 1, no = 0):

| # | Question | Key |
|---|---------|-----|
| 1 | Is the change above the fold or in the primary viewport? | `above_fold` |
| 2 | Is it backed by quantitative data (analytics, ad data, ShopifyQL)? | `quant_data` |
| 3 | Is it backed by qualitative or behavioural data (Clarity, replays, surveys)? | `qual_data` |
| 4 | Does it affect a page with 1,000+ sessions/month? | `high_traffic` |
| 5 | Is it a bug or technical fix? (Broken = ship immediately, no test) | `bug_fix` |
| 6 | Does it directly affect the primary conversion action (ATC, checkout, purchase)? | `primary_action` |
| 7 | Is the change noticeable to a visitor within 5 seconds? | `noticeable_5s` |

**Maximum score: 7**

**Scoring rules:**
- If `bug_fix = YES`: automatically assign TIER 3 regardless of total score (bugs get fixed, not tested)
- If `quant_data = NO` AND `qual_data = NO`: maximum tier is TIER 4 (no evidence = no test)
- Traffic check: before assigning any A/B test, calculate sample size (see below)

---

## Step 3: Sample size check for A/B tests

Before recommending any A/B test, confirm the page has enough traffic to reach significance in 4 weeks.

**Formula:**
```
sessions_required_per_variant = (16 × p × (1 - p)) / MDE²
```

Where:
- `p` = baseline conversion rate for that page/step (from store data)
- `MDE` = minimum detectable effect — use 10% relative by default
  - Exception: use larger MDE (20–50%) only when there is strong prior evidence that the change will have a large effect (e.g. making an invisible button visible)
  - Must justify any MDE > 10% in the output

**Check:**
```
sessions_available_per_variant = monthly_page_sessions / 2
runtime_days = (sessions_required × 2) / (monthly_sessions / 30)
```

If `runtime_days > 28`: not enough traffic → downgrade to TIER 3 (ship directly).

---

## Step 4: Tier classification

| Score | Traffic | Tier | Action |
|-------|---------|------|--------|
| 6–7 | High (≥1K sessions/page/month) | **TIER 1** | A/B test, ship within 1 sprint |
| 4–5 | High | **TIER 2** | A/B test, next sprint |
| Any | Low effort + Low risk (bug fixes, copy, config) | **TIER 3** | Ship directly, no test needed |
| Any | Low traffic (< 1K sessions/page/month) | **TIER 4** | Fix based on heuristics, no test |
| ≤ 3 | Any | **TIER 5** | Defer — not enough evidence or impact |

**Priority within tiers:** P0 bugs always first, regardless of PXL score.

---

## Step 5: Output — Quick Wins (TIER 3)

List all TIER 3 items in this format:

```
QUICK WIN: [issue_id]
Priority: P0 / P1 / P2
Title: [specific, one-line description]
Why ship without testing: [bug fix / low-risk config / copy change / clear best practice]
Effort: [time estimate]
Owner: [developer / marketing / designer / founder]
Fix:
  1. [Step 1]
  2. [Step 2]
  3. [Step 3]
Expected outcome: [specific metric improvement or revenue estimate]
```

Order by: P0 first, then by effort (shortest first).

---

## Step 6: Output — A/B Test Roadmap (TIER 1 and TIER 2)

For each test:

```
TEST: [hypothesis_id]
Tier: 1 / 2
PXL Score: [X/7]
Page: [page name + URL pattern]
Monthly page sessions: [number from store data]

Hypothesis:
  If we [change X],
  then [metric Y] will [increase/decrease by Z%],
  because [specific evidence from audits].

Control: [description of current state]
Variant: [description of proposed change]

Primary metric: [specific KPI — e.g. "add-to-cart rate on this PDP"]
Secondary metrics: [1–2 supporting metrics]

Sample size calculation:
  Baseline CVR: [p]%
  MDE: [X]% relative ([Y]% absolute)
  MDE justification: [why this MDE is valid]
  Sessions required per variant: [number]
  Available per variant: [monthly_sessions / 2]
  Estimated runtime: [days]

Sprint: 1 / 2 (TIER 1 = Sprint 1, TIER 2 = Sprint 2)
```

**Sprint rules:**
- Never run more than 2 A/B tests simultaneously on the same traffic pool
- Run tests sequentially on low-traffic stores (< 10K sessions/month)
- Tests in TIER 1 go into Sprint 1; TIER 2 into Sprint 2

---

## Step 7: Output — Deferred Backlog (TIER 5)

Brief list only. No detailed spec needed — these won't be actioned soon.

Format:
```
DEFERRED: [issue_id]
Why deferred: [score too low / insufficient traffic / too complex / dependency on other fix]
Revisit when: [specific condition — e.g. "when monthly sessions > 20K" or "after retargeting is set up"]
```

---

## Step 8: Output — Sprint 1 Developer Briefing

Write to `output/sprint1_briefing.md`.

Format:

```markdown
# Sprint 1 CRO Briefing
Generated: [date]
Store: [store name]

## Summary
- X quick wins to ship this sprint
- Y A/B tests to set up
- Total estimated monthly impact: ₹[range]

## P0 Items (ship immediately, before anything else)
[List of P0 bugs with exact fix steps]

## Quick Wins (ship without testing)
[All TIER 3 items with full fix steps]

## A/B Tests to Set Up
[All TIER 1 items with full test spec]

## Dependencies
[Any items that are blocked on other items completing first]

## What to track after implementing
[Specific metrics to monitor for each change — how to know if it worked]
```

---

## Step 9: Regenerate dashboard

After scoring is complete, run:
```bash
python3 cro_agent.py
```

This regenerates `cro_dashboard.html` with all scored issues.

---

## Scoring table template

Produce a summary table before detailed output:

| Issue ID | Title (short) | P | Score | Tier | Est. Impact |
|----------|--------------|---|-------|------|-------------|
| `meta_pixel_broken` | Meta Pixel firing 0 events | P0 | bug | T3 | ROAS tracking |
| `no_abandonment_email_sequence` | No cart recovery emails | P0 | 6/7 | T3 | ₹59K–₹79K/mo |
| `atc_button_hierarchy` | ATC button below fold mobile | P1 | 6/7 | T1 | +8–15% ATC rate |
| ... | | | | | |

Sort by: P0 first, then Tier (1 → 5), then score descending.
