# Case Study: Adorn Silver Atelier

**Store:** [adornsilver.co](https://www.adornsilver.co)
**Category:** Premium silver jewellery + gifting (D2C + B2B), India
**Revenue:** ₹3.37 Cr (FY26), 23× growth in 2 years
**Scan date:** May 2026

---

## Context

Adorn Silver is a fast-growing premium silver gifting brand out of Nagpur, India. Heritage Coins, Moments Card Sets, Banyan Tree bars, engraved jewellery. The kind of brand that grows through word of mouth, corporate gifting orders, and a strong WhatsApp sales motion.

They weren't failing. They were growing fast. But they'd never run a structured CRO audit. This was their first scan.

The scan took approximately 8 hours across 6 audits. Here's what it found.

---

## The business model surprise (Audit 1)

The most important finding came in the first audit.

When we looked at order referrer data, 97% of orders showed no HTTP referrer. In standard D2C analytics, this signals admin orders, WhatsApp shares, or direct traffic. For Adorn, it confirmed what was already partly known: **the online store is not primarily a checkout engine — it's a product catalogue that feeds WhatsApp sales.**

Customers browse the store, send a WhatsApp to the team, and close the order over chat (admin-entered). The store's blended AOV of ₹47,780 is meaningless as a D2C benchmark — it's inflated by large B2B and gifting orders closed by humans.

**Why this matters for CRO:** Most CRO advice assumes your conversion happens on-site. At Adorn, conversion happens off-site. This doesn't mean CRO doesn't apply — it means the levers are different. Reducing checkout friction still matters. But improving WhatsApp recovery sequences and cart-to-WhatsApp handoffs matter more.

---

## Critical bugs (P0 findings)

### Meta Pixel: 6+ weeks of zero purchase tracking

**Audit 1 finding.**

April 2026: ₹30,200 in Meta ad spend. 0 tracked purchase events.

Meta Events Manager showed the pixel was installed. Shopify confirmed orders were being placed. But purchase events weren't firing. The campaigns were optimising on zero signal — effectively running blind.

Every campaign's lookalike audiences, conversion optimisation, and ROAS calculations had been based on wrong data for at least 6 weeks.

**Fix:** Reinstall the Meta pixel via Shopify's native Facebook & Instagram app (not manual code injection). Takes 2 hours. **Fixed date: 2026-05-20.**

---

### Shopflo payment tracking: broken

**Audit 3 finding.**

Shopflo (the checkout tool) was not sending payment events back to the analytics stack. Orders were completing, but the conversion signal wasn't registering downstream.

This compounds the Meta Pixel issue: even if the pixel had been firing correctly, the checkout wasn't sending the purchase event at the right moment.

---

### Google Ads: ₹6,868 spend, 0 conversions

**Audit 5 finding.**

One Google campaign had spent ₹6,868 over a 6-week period with zero tracked conversions. The campaign was still active at time of audit.

This is partly downstream of the tracking issues above — conversions may have occurred but weren't registering. But the discovery process matters: **nobody had looked at this campaign's performance in 6 weeks.**

---

## UX findings (P0–P1)

### ATC button invisible on 75% of mobile screens

**Audit 2 + Audit 4 finding.**

On mobile PDPs, the Add to Cart button was below the fold on all tested device sizes. Clarity session replays confirmed: 75%+ of mobile users land on a PDP and cannot see the ATC button without scrolling.

The button was there. It just wasn't visible.

**Context:** Mobile traffic is the majority of Adorn's visits. The button that converts visitors to buyers was hidden from most of them.

**Fix:** ATC button pinned to bottom of viewport on mobile (sticky). Shopify theme setting — 30 minutes to implement.

---

### Hero section: 0 CTAs on 100% of paid traffic landing page

**Audit 2 finding.**

The homepage hero is a full-bleed slideshow — "Cosmic Love Collection" — with beautiful imagery and zero clickable elements. Every visitor who lands on the homepage from a paid ad sees a billboard with no door.

The collection is featured. The product is visible. But there's no button that says "Shop this collection" or "See all designs."

**Fix:** Add CTA button to each hero slide. 30 minutes in Shopify theme customiser.

---

### Checkout OTP wall: estimated ₹28L/month invisible abandonment

**Audit 3 finding — the biggest structural issue.**

Shopflo's checkout flow requires phone number + OTP verification before payment. Users who enter their phone number and then abandon never complete the OTP step.

**The consequence:** Shopify's abandoned checkout system only captures abandonments after cart creation. Shopflo OTP-stage abandonments happen before a Shopify cart is created — so they never appear in Shopify's abandoned checkout reports.

Shopify showed 20 abandoned checkouts in 30 days, totalling ₹3.94L.

Estimated actual abandonment: ~303 total abandonments. The "invisible" 283 represent an estimated ₹28L in abandonment value that Shopify's analytics couldn't see — and therefore no recovery sequence was targeting.

**Fix options:**
- Enable Shopflo's ACR (Abandoned Checkout Recovery) module — it has the phone numbers, can send WhatsApp recovery
- Shopflo Dashboard → ACR survey → enable WhatsApp re-engagement sequence

---

## Revenue leakage findings (Audit 6)

### No abandonment email sequence

Shopify's native abandoned checkout email automation was not enabled. 20 tracked abandonments (₹3.94L) per month, zero follow-up sent.

Industry recovery rate for triggered email sequences: 15–20%.

**Potential:** ₹59K–₹79K/month in recovered revenue. **Effort to implement:** 2 hours in Shopify Admin.

This is the highest-ROI finding in the audit. A 2-hour configuration change with ₹59K–₹79K/month upside.

---

### No post-purchase upsell

After checkout, customers see a generic thank-you page. No upsell offer. No product recommendation.

Post-purchase is the highest-intent moment in the funnel — the customer just paid, the card is warm, there's no friction. And Adorn's catalogue has natural set completions: Heritage Coin + chain, Moments Card + premium box, engraved tag + pendant.

**Potential:** ₹15K–₹30K/month (5–15% take rate on 200 D2C orders at ₹499–₹999 offer price).

---

### No free shipping progress bar

Free shipping threshold: ₹10,000. Average D2C order: ₹9,843.

Most D2C customers are within ₹157–₹2,000 of free shipping. There's no cart-level nudge showing how close they are.

With 74 orders per month in the ₹6K–₹10K range, converting 30% of them to ₹10,000+ would add ₹65K/month in revenue. A cart progress bar is a 1-hour implementation.

---

## Phase 5 results: scored findings

After all 6 audits, 29 confirmed issues were scored using the PXL framework.

**Quick wins (TIER 3 — ship without A/B testing): 20 issues**

The 20 lowest-effort, highest-confidence fixes that should be shipped immediately:

| Issue | Effort | PXL Score |
|-------|--------|-----------|
| Enable abandoned checkout email sequence | 2h | 8/10 |
| Add hero CTAs to homepage slideshow | 30m | 6/10 |
| Sticky ATC button on mobile PDPs | 30m | 8/10 |
| Announcement bar: free shipping threshold | 15m | 7/10 |
| Shopflo: enable trust badges | 30m | 6/10 |
| Fix Meta Pixel via native Shopify app | 2h | P0 bug |
| ... 14 more | | |

**A/B test roadmap (TIER 1–2): 3 tests**

Traffic constraint: ~10,000 sessions/month total limits concurrent testing.

| Hypothesis | Traffic | MDE | Est. runtime |
|-----------|---------|-----|-------------|
| Sticky ATC button (mobile PDPs) | 2,738/mo | 50% relative | 22 days |
| Hero CTA button (homepage) | 5,000/mo | 15% relative | 28 days |
| Moments Card occasion variants: chips vs dropdown | PDP traffic | 15% relative | 28 days |

---

## Total estimated monthly impact

| Category | Monthly Opportunity |
|----------|-------------------|
| Abandoned checkout email recovery | ₹59K–₹79K |
| WhatsApp abandonment recovery (Shopflo) | ₹42K–₹84K |
| Cart AOV lift (shipping threshold nudge) | ₹25K–₹40K |
| Post-purchase upsell | ₹15K–₹30K |
| Gift wrap add-on | ₹5K–₹12K |
| Meta Pixel fix → ROAS improvement | Indirect (₹30K+ spend now trackable) |
| **Total** | **₹1.46L–₹2.45L/month direct** |

Plus the indirect impact of fixing tracking (Meta Pixel, Shopflo payment tracking) which affects every future campaign's optimisation capability.

---

## What didn't exist before this scan

- No systematic record of issues and when they were first detected
- No PXL-scored prioritisation — everything was "gut feel" importance
- No developer briefing document — fixes were discussed in WhatsApp, not tracked
- No sample size calculation — A/B tests were launched without knowing if traffic could reach significance

After the scan:
- `data/issue_statuses.json` — 29 issues tracked, dated, with fix history
- `output/cro_dashboard.html` — visual issue board
- `output/sprint1_briefing.md` — 20 quick wins with exact implementation steps, developer-ready

---

## Lessons for other stores

**1. Analytics gaps compound silently.** A broken pixel doesn't announce itself. It just makes every ad decision worse, quietly, for months.

**2. Your "abandoned cart" number is probably an undercount.** If you use a checkout tool with phone capture before cart creation, you have an entire category of abandonments that Shopify can't see.

**3. The highest-ROI CRO changes are often configuration, not design.** Enabling an email sequence (2 hours) vs redesigning a landing page (2 weeks). The email sequence will outperform the landing page redesign on ROI almost every time.

**4. Traffic constraints determine your testing strategy.** Most small Shopify stores can't run A/B tests on most pages — they don't have enough sessions to reach significance in 4 weeks. Knowing this upfront means shipping fixes directly instead of waiting for tests that will never conclude.

**5. Business model first.** The most important finding was understanding the WhatsApp-first sales motion. Without that context, you'd try to optimise the checkout for volume — when the real lever is optimising the WhatsApp handoff and post-conversation follow-up.
