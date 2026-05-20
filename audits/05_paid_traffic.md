# Audit 5 — Paid Traffic

**Goal:** Find where ad spend is being wasted, identify landing page mismatches, and check whether ROAS is being measured correctly given the tracking state found in Audit 1.

**Requires:** Windsor.ai MCP, Meta Ads MCP, or Google Ads MCP

**Important:** Run this audit after Audit 1. If tracking is broken (as found in Audit 1), ROAS numbers in this audit will be understated. Note the tracking state when interpreting every metric here.

---

## Phase A: Spend efficiency by campaign

Pull last 30 days of campaign data.

**Meta Ads:**
```
Source: facebook_ads
Fields: campaign_name, spend, clicks, impressions, conversions, conversion_value
Date range: last 30 days
```

**Google Ads:**
```
Source: google_ads
Fields: campaign_name, spend, clicks, impressions, conversions, conversion_value
Date range: last 30 days
```

**For each campaign, calculate:**
- ROAS = `conversion_value / spend`
- CPA = `spend / conversions`
- CTR = `clicks / impressions`

**Flag:**
- Any campaign with spend > ₹1,000 and 0 conversions → P0 (could be tracking issue or genuinely broken)
- Any campaign with CPA > 3× store AOV → unsustainable
- Any campaign running for > 2 weeks with ROAS < 1 → burning money

---

## Phase B: Zero-conversion spend audit

Identify all campaigns/ad sets with > ₹500 spend and 0 tracked conversions over last 30 days.

For each zero-conversion item:
1. Check: is this a tracking issue (Audit 1 showed pixel problems)?
2. Check: what is the landing page? (URL the ad links to)
3. Check: what is the ad creative promising?
4. Check: does the landing page deliver on that promise?

If it's a tracking issue: still flag the campaign for review, but note that conversions may exist but aren't tracked.

If it's genuinely zero conversions with working tracking: this is a P0 spend waste issue.

---

## Phase C: Landing page relevance check

For the top 5 campaigns by spend:

Pull the destination URL from the ad creative.

**Check:**
- Does the ad headline match the landing page headline? (Relevance — LIFT model)
- Does the ad image match the landing page hero image?
- If the ad promotes a specific product/collection: does it land on that collection/product page, or the homepage?

**Homepage as landing page is almost always wrong for campaign traffic:**
- Campaign traffic has specific intent (came from a specific ad about a specific product)
- Landing on the homepage forces them to re-discover what they came for
- Exception: brand awareness campaigns, where homepage is intentional

**Flag:** Any campaign with specific product/collection creative that lands on the homepage (`paid_social_lp_mismatch`).

---

## Phase D: Audience and targeting review

**Meta:**
- Are there overlapping audiences across ad sets? (Causes auction cannibalisation)
- Is retargeting running? (People who visited but didn't buy — typically 3–5× ROAS vs cold audiences)
- Are lookalike audiences based on buyers or visitors? (Buyer lookalikes outperform visitor lookalikes)

**Google:**
- Which match types are running? (Broad match on high-intent branded terms bleeds spend)
- Are branded keywords protected? (If running non-branded campaigns and not protecting brand terms, competitors can bid on your brand name)
- Is Performance Max running? (PMax can cannibalise existing campaigns)

---

## Phase E: Budget pacing

Check: is spend distributed evenly, or are there day-of-week patterns?

**Pull daily spend breakdown:**
- Are weekends significantly different from weekdays?
- Are there days with zero spend (budget exhausted by mid-day)?

Daily budget exhaustion means you're losing traffic during peak hours while paying for off-peak hours.

---

## Phase F: Creative performance

If time allows, check creative-level performance:

- Which creatives have the highest CTR?
- Which creatives have the lowest CPA?
- Are there creatives running with < 100 impressions? (Insufficient data — algorithm hasn't tested them)
- Are there creatives that haven't been refreshed in > 4 weeks? (Creative fatigue)

---

## Output format

```
FINDING: [issue_id]
Platform: meta / google / both
Campaign: [specific campaign name or "all campaigns"]
Priority: P0 / P1 / P2
Evidence: [spend amount, conversion count, ROAS, specific numbers]
Tracking context: [note if tracking issues from Audit 1 affect interpretation]
Hypothesis: [If we change X, ROAS/CPA will improve by Y because evidence]
Impact: [₹ monthly waste identified OR ₹ recoverable revenue]
Fix steps: [numbered, specific]
```

**Update `data/issue_statuses.json`** with any new issues found.

---

## Common issues and IDs

| Issue | ID |
|-------|-----|
| Campaign with spend and 0 conversions | `[platform]_zero_conversion_campaign` |
| Paid social ads landing on homepage | `paid_social_lp_mismatch` |
| Meta pixel not tracking purchases | `meta_pixel_broken` / `meta_pixel_incomplete` (cross-reference Audit 1) |
| No retargeting campaign running | `no_retargeting_campaign` |
| Creative fatigue (> 4 weeks same creative) | `[platform]_creative_fatigue` |
| Budget exhausting intra-day | `[platform]_budget_exhaustion` |
