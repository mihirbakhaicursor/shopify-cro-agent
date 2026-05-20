# Audit 1 — Analytics Health

**Goal:** Confirm that every conversion event is being tracked accurately. Find tracking gaps before drawing any conclusions about the store's performance.

Analytics is the foundation. If it's broken, every insight built on top of it is wrong.

---

## Phase A: Pixel and purchase event verification

Pull from the ad account MCPs:

**Meta:**
- Total purchase events in the last 30 days
- Compare to Shopify order count for the same period
- Calculate match rate: `pixel_purchases / shopify_orders`
- Flag if match rate < 85%

**Google:**
- Total conversion events (purchase) in the last 30 days
- Compare to Shopify order count
- Flag if match rate < 80%

**Red flags:**
- Match rate < 50% → tracking is critically broken
- Match rate 50–80% → partial tracking issue
- Match rate > 80% → acceptable (some discrepancy is normal due to ad blockers, iOS privacy)
- Match rate 0% with active ad spend → pixel is broken, P0 issue

---

## Phase B: Mobile vs desktop conversion gap

Pull from Shopify MCP (ShopifyQL):
```
FROM sessions
SELECT device_type, sessions, orders, conversion_rate
WHERE date >= 30_days_ago
GROUP BY device_type
```

**Questions to answer:**
- What is mobile CVR vs desktop CVR?
- Is the mobile CVR gap larger than expected? (Industry benchmark: mobile CVR typically 40–60% of desktop for most Shopify stores)
- Could any of the gap be explained by tracking issues (Shopify sessions vs GA4 sessions on mobile)?

**Flag if:** Mobile CVR < 30% of desktop CVR — this usually indicates either a tracking gap or a severe UX problem on mobile (proceed to Audits 2 + 4 to distinguish).

---

## Phase C: Revenue attribution

Pull from Shopify MCP:
```
FROM orders
SELECT source_name, COUNT(*), SUM(total_price)
WHERE date >= 30_days_ago
GROUP BY source_name
```

**Questions to answer:**
- What % of orders come from "web" vs "pos" vs "admin" vs "draft_orders"?
- Is there a meaningful split between online orders and admin/WhatsApp orders?
- If admin/WhatsApp orders dominate (>50%), flag this: the store may be primarily a WhatsApp-assisted sales channel, not a self-serve checkout funnel. This changes which CRO levers matter most.

---

## Phase D: UTM and landing page coverage

Check: are UTM parameters being consistently applied to paid traffic links?

Pull top landing pages from GA4 or Windsor:
- What % of paid sessions have UTM source/medium/campaign populated?
- Are campaign names consistent enough to be useful for analysis?

**Flag if:** >30% of paid sessions show no UTM — attribution data is unreliable.

---

## Output format

For each finding:

```
FINDING: [issue_id]
Priority: P0 / P1 / P2
Evidence: [specific numbers]
Hypothesis: [If we fix X, Y will improve by Z because evidence]
Impact: [estimate based on actual store data]
Effort: [honest time estimate]
Fix steps: [numbered, actionable]
```

**Update `data/issue_statuses.json`** with any new issues found.

---

## Common issues and IDs to use

| Issue | ID |
|-------|-----|
| Meta Pixel firing 0 purchase events | `meta_pixel_broken` |
| Meta Pixel fires but incomplete (no value/currency) | `meta_pixel_incomplete` |
| Mobile CVR gap vs desktop unexplained | `mobile_cvr_gap` |
| No UTM coverage on paid traffic | `attribution_discrepancy` |
| Paid social traffic landing on homepage (mismatch) | `paid_social_lp_mismatch` |
| Google pixel/tag not tracking purchases | `google_pixel_broken` |
