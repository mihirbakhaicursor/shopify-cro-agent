# Audit 4 — Behavioural

**Goal:** Use session recording and heatmap data to find where visitors are actually going, what they're clicking, where they're dropping off, and what's frustrating them. This is the "ground truth" layer — it validates or contradicts the heuristic findings from Audit 2.

**Requires:** Microsoft Clarity MCP (or equivalent: Hotjar, FullStory, Lucky Orange)

---

## Phase A: Scroll depth

Pull scroll depth data for each key page over the last 30 days.

**Pages to check:**
- Homepage
- Primary collection/PLP
- Top 3 PDPs by traffic
- Cart page

**Questions to answer:**
- What % of visitors scroll past 50% of the page?
- What % of visitors scroll past 75% of the page?
- Where does the biggest scroll drop-off occur?

**Why this matters:**
If 60% of visitors exit before scrolling past the hero, everything below the hero is effectively invisible — social proof, product features, reviews, CTAs. Content that's "on the page" but below the average fold depth is not being seen.

**Thresholds:**
- < 30% scrolling past 50%: severe fold problem, content is not compelling visitors to explore
- 30–60% scrolling past 50%: moderate — check what's at the 50% point
- > 60% scrolling past 50%: good engagement

**How to interpret:**
Note the page height at the average fold depth (varies by device). Map this against what content is actually at that position. Often the drop-off is right where something annoying appears (interstitial, popup, slow-loading section) rather than just "end of interest."

---

## Phase B: Click maps and rage clicks

Pull click heatmap data for:
- Homepage
- Primary PDP
- Cart

**Look for:**

**Rage clicks** (multiple fast clicks on same element):
- Element that looks clickable but isn't (e.g., product description text, non-linked images)
- Element that is supposed to be clickable but has a bug
- CTA button that isn't responding fast enough (perceived lag)

**Dead clicks** (clicks on elements that do nothing):
- Areas where visitors consistently click expecting something to happen
- Navigation elements that don't lead where visitors expect

**Surprising clicks:**
- Visitors clicking something you didn't expect — this reveals intent
- Visitors not clicking something you thought was obvious — this reveals visibility failure

---

## Phase C: Session replays on high-exit pages

Identify the 2–3 pages with the highest exit rate from ShopifyQL:
```
FROM sessions
SELECT landing_page, exit_rate
WHERE date >= 30_days_ago
ORDER BY exit_rate DESC
LIMIT 10
```

Watch 5–10 session replays on each high-exit page.

**What to look for:**
- Where does the session end? (Rage click? Scroll to bottom and back? Hit the ATC then leave?)
- Is there any visible moment of confusion? (Multiple clicks on one area, scrolling back up)
- Does the visitor find what they came for?
- On mobile: are any interactive elements too small to tap? (< 44px touch targets)

**Document patterns:** If the same exit behaviour appears in multiple replays, it's a pattern, not a one-off.

---

## Phase D: Mobile vs desktop behaviour

Pull separate heatmaps/scroll data for mobile and desktop if available.

**Key comparison:**
- Is the ATC button visible above fold on mobile? (Check the 50th percentile scroll depth — if users are reaching it, the button is probably visible; if they're exiting before then, it may not be)
- Are tap targets on mobile large enough? (Session replays: look for repeated attempts to tap small elements)
- Is navigation usable on mobile? (Hamburger menu accessible, dropdowns functional)

---

## Phase E: Form and funnel drop-off

If Clarity captures checkout funnel data:
- Where does the biggest drop-off occur in the checkout flow?
- Step 1 (contact info) → Step 2 (shipping) → Step 3 (payment) — which transition loses the most users?

If Clarity doesn't capture checkout (common when using third-party checkout tools like Shopflo):
- Note this gap: checkout funnel is a black box
- Recommend checking the checkout tool's own analytics for step-by-step drop-off

---

## Output format

For each finding, map it back to a heuristic or technical finding if possible (confirming or contradicting):

```
FINDING: [issue_id]
Page: [page]
Behavioural signal: scroll_depth / rage_click / dead_click / session_replay / funnel_drop
Priority: P0 / P1 / P2
Evidence: [specific metric — "72% of homepage visitors exit before scrolling past 400px, which is where the first CTA appears"]
Confirms: [links to Audit 2 or 3 finding if this validates it]
Hypothesis: [If we change X, Y will improve because this behavioural data shows Z]
Fix steps: [numbered, specific]
```

**Update `data/issue_statuses.json`** with any new issues found.

---

## Common issues and IDs

| Issue | ID |
|-------|-----|
| ATC button below fold on mobile | `atc_button_hierarchy` (confirms Audit 2) |
| Hero has no CTA, high exit rate | `hero_no_cta` (confirms Audit 2) |
| Rage clicks on non-interactive element | `[page]_rage_click_[element]` |
| Low scroll depth on key page | `[page]_low_scroll_depth` |
| Checkout funnel drop at OTP step | `shopflo_otp_wall` (confirms Audit 3) |
