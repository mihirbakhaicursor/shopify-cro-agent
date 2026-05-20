# Your First CRO Scan

This is a guide for running a complete CRO audit on your Shopify store for the first time. It takes 2–4 hours. At the end, you will have:

- A list of every confirmed issue on your store, with evidence
- A score and priority level for each issue
- A sprint briefing document your developer can execute from

Most stores find 15–25 issues in their first scan. A few of them will be obvious once you see them. Most won't be — they're invisible in your day-to-day analytics but visible the moment you look with the right questions.

---

## Before you start

**Set aside 2–4 hours.** You don't need to do it all at once — the agent saves state between sessions. But each audit works better when completed in one sitting.

**Have these open:**
- Claude Code (with Shopify MCP connected)
- Your Shopify admin in a browser tab
- Microsoft Clarity (if connected) — free to set up at clarity.microsoft.com
- Your ad account dashboards (Meta / Google) if you're running paid traffic

**Complete `store_config.json` first.** Even rough numbers help the agent size the impact of findings correctly. A missing session count means it can't tell you whether you have enough traffic for A/B testing.

---

## The 6 audits — what each one looks for

### Audit 1 — Analytics Health (~20 minutes)
*This is where most scans find their first surprise.*

Analytics health is boring until it isn't. A tracking gap means every decision you've made for the past N weeks has been based on wrong data. This audit checks:

- Is your pixel / GA4 tag firing on every order?
- Are you seeing purchase events in your ad accounts?
- Is mobile conversion rate artificially low (tracking gap vs real gap)?
- Is attribution broken in a way that's hiding the true cost of paid channels?

**What good looks like:** Purchase events in Meta Events Manager match Shopify orders within 10–15%. Session counts in GA4 match Shopify sessions within 20%.

**What broken looks like:** ₹30K/month in Meta spend, 0 tracked purchases. (This is what we found on the real store. The pixel had been broken for 6+ weeks. Every ad was optimising toward nothing.)

---

### Audit 2 — Heuristic Review (~30–45 minutes)
*The "obvious when you know what to look for" audit.*

This is a structured walkthrough of your store using two frameworks:

**LIFT Model** — 6 factors that determine whether a visitor converts:
- Value Proposition — is it clear why they should buy from you?
- Relevance — does the page match what they came looking for?
- Clarity — is it obvious what to do next?
- Anxiety — what's making them hesitate?
- Distraction — what's pulling attention away from the conversion?
- Urgency — why now?

**7 Levels of Conversion (André Morys):**
- Level 1: Relevance — "Is this for me?"
- Level 2: Trust — "Can I trust this brand?"
- Level 3: Orientation — "Where do I go next?"
- Level 4: Stimulation — "Do I want this?"
- Level 5: Security — "Is it safe to buy?"
- Level 6: Convenience — "Is it easy to buy?"
- Level 7: Confirmation — "Did I make the right choice?"

The agent walks your homepage, collection page, product pages, and checkout against these frameworks and surfaces gaps.

**Common findings here:**
- Hero section has beautiful imagery but no CTA button
- Product page doesn't answer "why this brand over Amazon" anywhere visible
- Delivery policy and return policy buried in footer — not near the buy button
- Trust signals (reviews, certifications) exist but are below the fold

---

### Audit 3 — Technical (~30 minutes)
*Where speed problems and silent errors live.*

The agent runs PageSpeed Insights against your homepage and key product pages, and queries your checkout tool's error logs.

**What it checks:**
- Mobile Speed Score and Core Web Vitals (LCP, FCP, TBT)
- Image format and compression (WebP vs JPEG/PNG)
- Script bloat and third-party tag weight
- JavaScript errors in the browser console
- Checkout-specific issues (payment tracking, trust badges, OTP flows)

**A real example:** On the Adorn scan, we found that the checkout's OTP wall was capturing phone numbers from users who then abandoned — but those abandonments never showed up in Shopify's abandoned checkout system. The store thought it had 20 abandoned checkouts/month. The real number was ~303.

---

### Audit 4 — Behavioural (~30 minutes, requires Clarity)
*What your visitors are actually doing.*

Microsoft Clarity is free and records every session. This audit uses it to find:

- Scroll depth on key pages (how far do people actually scroll?)
- Rage clicks (where are people clicking that doesn't work?)
- Dead clicks (where are people clicking that does nothing?)
- Session replays on high-exit pages

**What scroll depth tells you:** If 60% of visitors exit the homepage without scrolling past the hero, everything below the hero is effectively invisible — no matter how good the content is.

**What rage clicks tell you:** If visitors are rage-clicking an element, it's either broken, or it looks clickable but isn't. Both are conversion killers.

---

### Audit 5 — Paid Traffic (~30 minutes, requires ad account MCP)
*Is your ad spend working?*

This audit pulls data from Meta and Google Ads to find:

- Campaigns with high spend and zero conversions
- Landing page mismatch (ad says X, page says Y)
- Audience overlap between campaigns
- ROAS by campaign and whether it justifies the spend

**A real example:** The Adorn scan found a Google campaign with ₹6,868 in spend and 0 tracked conversions over 6 weeks. The campaign was still running. Nobody had looked at it.

---

### Audit 6 — Revenue & AOV (~45 minutes)
*Where the money is leaking.*

This audit focuses on revenue that exists but isn't being captured:

- Abandoned checkout recovery (email sequences, WhatsApp flows)
- Average order value — what's dragging it down, what would lift it?
- Post-purchase upsell — is there any?
- Repeat purchase rate and what's stopping customers from coming back
- Product pricing gaps and bundle opportunities

**The key insight from the Adorn scan:** The store had ₹3.94L/month in abandoned checkouts with zero recovery emails sent. The Shopify native abandonment sequence wasn't enabled. This takes 2 hours to fix.

---

## Phase 5 — Scoring and prioritisation (~30 minutes)

After all 6 audits, the agent scores every finding using the PXL framework (binary scoring — no subjective 1-10 guesswork) and sorts them into:

**Quick Wins** — ship this week, no A/B test needed
**A/B Test Roadmap** — experiments to run in order, with sample size calculations
**Deferred backlog** — good ideas that need more traffic or resources

The output is `output/sprint1_briefing.md` — a document your developer can open and start executing from Monday.

---

## What happens to your data

Everything stays local. The agent reads from your connected MCPs and writes findings to:
- `data/issue_statuses.json` — the issue tracker
- `output/cro_dashboard.html` — visual issue dashboard
- `output/sprint1_briefing.md` — developer briefing

Nothing is sent anywhere. Your store data doesn't leave your machine.

---

## Running the scan

```
"Run a first CRO scan on my store"
```

Or to run individual audits:
```
"Run Audit 1 — Analytics Health"
"Run Audit 3 — Technical"
"Score all findings from Audits 1-3 using PXL"
```

---

## What to do with the results

1. **Read the Quick Wins list.** These are high-confidence fixes that can ship without A/B testing. Your developer should be able to complete most of them in a day or two.

2. **Look at the P0 findings first.** P0 means "this is breaking something that should work." A broken pixel, a JS error in checkout, an abandoned cart sequence that's disabled — fix these before anything else.

3. **Review the A/B test roadmap.** If you have enough traffic (usually 5,000+ sessions/month per page), start with the highest-PXL-score test. If not, most things should just ship.

4. **Schedule a re-scan.** Run this every 4–8 weeks. The `issue_statuses.json` tracks when each issue was first detected and when it was fixed — so you can see the before/after impact in PageSpeed and analytics.

---

## First scan checklist

- [ ] `store_config.json` filled in with real numbers
- [ ] Shopify MCP connected
- [ ] Clarity MCP connected (if you have Clarity installed — if not, [install it first](https://clarity.microsoft.com), free)
- [ ] Ad account MCPs connected (if running paid traffic)
- [ ] 2–4 hours blocked
- [ ] Quick wins actioned within 1 week of scan
- [ ] Developers briefed from `output/sprint1_briefing.md`

---

Ready to start? Open Claude Code in this directory and say: **"Run a first CRO scan on my store."**
