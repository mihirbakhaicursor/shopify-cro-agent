# Audit 2 — Heuristic Review

**Goal:** Walk every key page of the store through two structured frameworks and surface UX gaps that are suppressing conversions. No analytics data required — this is expert review against proven CRO frameworks.

---

## Frameworks to apply

### LIFT Model (6 factors)
Score each factor for each page: **strong / weak / missing**

| Factor | Question |
|--------|----------|
| **Value Proposition** | Is it immediately clear why to buy from this store vs alternatives? |
| **Relevance** | Does the page match what the visitor came for? |
| **Clarity** | Is it obvious what to do next? |
| **Anxiety** | What is creating hesitation or doubt? |
| **Distraction** | What is pulling attention away from the conversion action? |
| **Urgency** | Is there any reason to act now rather than later? |

### 7 Levels of Conversion (André Morys)
Map each page issue to the level it affects:

| Level | Name | Question |
|-------|------|----------|
| 1 | Relevance | "Is this for me?" |
| 2 | Trust | "Can I trust this brand?" |
| 3 | Orientation | "Where do I go next?" |
| 4 | Stimulation | "Do I want this?" |
| 5 | Security | "Is it safe to buy?" |
| 6 | Convenience | "Is it easy to buy?" |
| 7 | Confirmation | "Did I make the right choice?" |

---

## Page review order

**Do not review pages in a fixed sequence.** Use the Page Priority Stack from `audits/00_page_priority.md`.

- **Tier 1 pages first** — review all of them in full
- **Tier 2 pages** — review if time allows, or if the user flags them
- **Tier 3 pages** — skip unless specifically requested

If the Page Priority Map hasn't been run yet, run it now before proceeding.

Every finding in this audit must note which page tier it's on. A broken CTA on a Tier 1 page (paid traffic, 4,000 sessions) is P0. The same issue on a Tier 3 page is P2.

---

## Page-by-page review

The checklist below covers what to look for on each page type. Apply it to each page in tier order, not in the order listed here.

### Homepage

**Check:**
- Is there a clear value proposition in the first viewport? (What you sell, why you're different, who it's for)
- Is there a visible CTA above the fold on desktop AND mobile?
- Are there trust signals near the top? (Ratings, customer count, certifications, press mentions)
- Is free shipping / returns policy visible without scrolling?
- Is the navigation clear? (Can a first-time visitor find what they're looking for in <5 seconds?)
- Is there any urgency signal? (Sale, limited edition, seasonal relevance)

**Common findings:**
- Hero is imagery-only with no CTA button (`hero_no_cta`)
- Trust signals exist but are below fold (`homepage_trust_strip_missing`)
- Free shipping threshold exists but isn't communicated above footer (`homepage_free_shipping_invisible`)

---

### Product Listing Page (PLP / Collection)

**Check:**
- Are products sorted by bestseller / most popular by default?
- Do product cards communicate enough to trigger a click? (Price, key specs, social proof badge)
- Are there any bestseller or "most loved" badges?
- Is the price range appropriate for the audience? (No sticker shock for first-time visitors)
- On mobile: how many products are visible without scrolling? (Target: 2–4)
- Is filtering/sorting functional and obvious?

**Common findings:**
- No bestseller badges (`plp_no_bestseller_badges`)
- No social proof on product cards (review count/rating not shown)
- Default sort order doesn't surface best-performing products

---

### Product Detail Page (PDP)

**Check (above fold on mobile):**
- Is the product name, price, and ATC button all visible without scrolling?
- Is the primary product image high quality and zoomable?
- Is there any trust signal near the ATC button? (Ratings, "X reviews", "Ships in X days")

**Check (below fold / full page):**
- Are delivery and return policy visible near the buy button (not just footer)?
- Is product description written for the customer or for the brand? (Benefits vs features)
- Is there a FAQ section addressing common pre-purchase objections?
- For products with variants: is the variant selector intuitive? (Chips vs dropdown matters)
- Is there a review section? Is it visible without excessive scrolling?

**Check button hierarchy:**
- Which button is visually primary — ATC or Buy It Now?
- ATC should be the solid/primary button; BIN should be secondary

**Common findings:**
- `atc_button_hierarchy` — BIN is solid/primary, ATC is outline/secondary
- `pdp_return_policy_hidden` — return policy only in footer, not near ATC
- `pdp_purity_below_fold` — key product spec (purity, BIS hallmark) not visible above fold
- `pdp_engraving_price_hidden` — custom engraving option price unclear or hidden
- Variant selector is dropdown when chips would be clearer

---

### Navigation

**Check:**
- Does the navigation cover all major product categories?
- Is there anything a first-time visitor would look for that's missing from nav?
- On mobile: is the hamburger menu accessible and complete?

**Common findings:**
- `nav_no_jewellery` — jewellery category missing from top nav while gifting items are featured

---

### Trust and social proof (site-wide)

**Check:**
- Is there a review count / aggregate rating visible on product cards and PDPs?
- Is there a "real customers" section (photos, testimonials)?
- Are certifications (BIS Hallmark, purity standards) mentioned clearly?
- Is there a brand story or "why us" section accessible from homepage?

---

## Output format

For each finding:

```
FINDING: [issue_id]
Page: homepage / plp / pdp / nav / site-wide
LIFT factor: Value Proposition / Relevance / Clarity / Anxiety / Distraction / Urgency
7-Level: 1-RELEVANCE through 7-CONFIRMATION
Priority: P0 / P1 / P2
Evidence: [what you observed — specific, not generic]
Hypothesis: [If we change X, metric Y will increase by Z because evidence]
Fix steps: [numbered, specific to this theme/store]
```

**Update `data/issue_statuses.json`** with any new issues found.
