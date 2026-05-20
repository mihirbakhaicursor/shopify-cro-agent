# Interpreting Your Findings

After your first scan, you'll have a list of issues with scores, priorities, and fix steps. Here's how to read them and decide what to do.

---

## Priority levels

**P0 — Something is broken right now**

This is not a "could be better" finding. This is "something that should work, doesn't." Examples:
- Pixel fires 0 purchase events despite real orders
- JavaScript error on every checkout page
- Abandoned checkout emails never enabled

P0s should be fixed before anything else. They're typically bugs or missing configurations, not design decisions. They don't require A/B testing — they require fixing.

If a P0 has sat unfixed for weeks (which tracking bugs often do), the compounding cost is high: every week of untracked conversions is a week of ad spend optimising toward nothing.

**P1 — High-impact opportunity with clear evidence**

Something is not broken, but it's clearly costing conversions. Examples:
- ATC button below fold on mobile (Clarity confirms 75% of visitors never see it)
- Hero section with no CTA (every paid traffic visitor lands on a page with no clear next step)
- No post-purchase upsell (zero incremental revenue at zero conversion risk)

P1s should be in Sprint 1. If they're TIER 3 (low effort, low risk), ship them without testing. If they're TIER 1 (high traffic, backed by data), set up an A/B test.

**P2 — Real opportunity, lower urgency**

Valid findings that should be actioned, but after P0 and P1 work is done. Examples:
- Free shipping threshold not communicated visibly
- No bestseller badges on PLPs
- Product variant selector as dropdown vs visual chips

---

## Tier system

**TIER 1 — A/B test, ship this sprint**

High PXL score (6–7/7) + enough traffic to reach significance in 4 weeks. These are your highest-confidence tests. Run them first.

**TIER 2 — A/B test, next sprint**

Medium PXL score (4–5/7) + enough traffic. Good ideas with solid-but-not-overwhelming evidence. Run after TIER 1 tests conclude.

**TIER 3 — Ship directly, no test**

Two paths lead here:
1. It's a bug fix — no need to test whether fixing a broken pixel "works"
2. Low effort + low risk + clear best practice — shipping it directly is better than waiting 4 weeks for a test to conclude on a 15-minute change

Most quick wins fall here. Don't overthink TIER 3. Ship it, monitor the metric, move on.

**TIER 4 — Fix based on heuristics, no test**

Low-traffic page. You can't get enough sessions to reach significance. Fix it based on best practices, document why you made the change, and look for signal in absolute numbers rather than A/B test results.

**TIER 5 — Defer**

Low score, low evidence, or too complex given current resources. Park it. Set a condition for revisiting ("when sessions > 15K/month" or "after checkout tracking is working").

---

## The revenue estimates

Every impact estimate in the output shows its working:

```
₹59K–₹79K/month recovered revenue
= 20 abandoned checkouts × ₹19,700 avg value × 15–20% recovery rate
```

The range (15–20%) comes from industry recovery rates for triggered email sequences. It's not guaranteed — it's a realistic expectation based on how abandonment recovery typically performs.

**How to use the estimates:**

- Use them to prioritise. ₹79K/month opportunity vs ₹5K/month opportunity — the ₹79K one goes first.
- Don't treat them as promises. The 15–20% recovery rate assumes a well-written 3-email sequence, not a generic Shopify default.
- The ₹ estimates assume current traffic levels. If traffic grows, the opportunity scales.

**When to be skeptical of an estimate:**
- The tracking data underlying it was incomplete (flag from Audit 1)
- The sample size is very small (< 20 orders in the relevant period)
- The assumption depends on a large behaviour change (e.g. "20% of visitors will click this new button" is optimistic without prior data)

---

## Sample size and A/B testing

**Why sample size matters:**

If you run an A/B test for 2 weeks and see a 15% uplift, you need to know whether that's real or noise. The sample size calculation tells you the minimum effect size you can reliably detect given your traffic.

A store with 2,000 sessions/month and a 2% CVR needs 3,200 sessions per variant to detect a 10% relative improvement. At 2,000 sessions/month, that's 32 months per test. This is why most small stores shouldn't run A/B tests on most pages — the math doesn't work.

**The solution:** Ship it directly (TIER 3) and watch what happens in absolute terms. If the cart recovery email generates ₹50K in month 1, it's working. You don't need a control group.

**When A/B testing is worth it:**
- High-traffic pages (homepage, top PDPs): 5,000+ sessions/month makes tests feasible in 4 weeks
- High-stakes changes: redesigning the checkout flow, changing pricing strategy, testing a new product layout — these justify the wait
- When you have a genuine hypothesis in two directions: you don't know if the change will help or hurt

**When to skip the A/B test:**
- It's a bug fix
- It's a best-practice change with overwhelming evidence (making an invisible button visible)
- The page doesn't have enough traffic to reach significance in 4 weeks
- The effort to set up the test exceeds the risk of just shipping it

---

## What to do the week after your scan

**Day 1–2:**
- Fix all P0 issues. These are blocking everything else.
- Enable the abandoned checkout email sequence (if not running). This takes 2 hours and pays back immediately.

**Day 3–5:**
- Ship all TIER 3 quick wins. Most take 15–60 minutes each. Your developer can knock out 5–10 in a day.

**End of week:**
- Brief your developer on the Sprint 1 document (`output/sprint1_briefing.md`)
- Set up any TIER 1 A/B tests if you have enough traffic

**In 4 weeks:**
- Re-scan the P0 items to confirm they're fixed
- Check abandonment recovery: how many emails sent, how many converted?
- Look at the A/B test results (if running)

**In 8 weeks:**
- Run a full re-scan
- `issue_statuses.json` will track which issues are still open vs fixed
- New issues (regressions, newly launched features) will surface

---

## When findings seem contradictory

Sometimes an audit will flag a problem, and when you go look, it seems fine. A few common reasons:

**"The pixel looks fine to me"** — Check Events Manager → Test Events with a real order, not just page load events. The pixel can be installed correctly but still not fire the Purchase event.

**"The scroll depth looks fine on desktop"** — Check mobile specifically. Scroll depth on desktop and mobile can differ dramatically, and most stores have more mobile traffic.

**"We do have abandonment emails"** — Confirm they're actually sending. Shopify Admin → Marketing → Automations → check "Sent" count in the last 30 days. A sequence can be "enabled" but have a misconfigured delay or condition that prevents sends.

**"Our ROAS looks good in the ad account"** — If the pixel is broken (Audit 1), the ad account ROAS is wrong. It's only counting the conversions it can see. True ROAS is likely lower.

When something doesn't match, trust the data trail over the interface. Follow the numbers.
