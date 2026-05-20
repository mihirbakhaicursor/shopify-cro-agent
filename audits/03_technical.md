# Audit 3 — Technical

**Goal:** Find speed problems, JavaScript errors, and checkout-specific technical issues that are silently killing conversions.

---

## Phase A: PageSpeed + Core Web Vitals

Run Google PageSpeed Insights on:
1. Homepage
2. Primary product page (highest-traffic PDP from ShopifyQL)
3. Collection page

For each page, record:
- Mobile Speed Score (flag if < 50)
- Desktop Speed Score (flag if < 70)
- First Contentful Paint / LCP (flag if LCP > 4s mobile)
- Total Blocking Time (flag if TBT > 500ms)
- Image format breakdown (flag if < 80% WebP)
- Script count (flag if > 80 scripts)
- Render-blocking resources

**API call:**
```
GET https://www.googleapis.com/pagespeedonline/v5/runPagespeed
  ?url=[PAGE_URL]
  &strategy=mobile
  &category=performance
```

---

## Phase B: Image audit

From PageSpeed results, identify:
- Total page weight (flag if > 2.5MB)
- Number of images not in WebP format
- Largest individual images (flag any > 100KB)
- Images with missing lazy loading

**Common findings:**
- `images_not_webp` — >20% of images are JPEG/PNG, inflating page weight
- Hero banner images > 500KB (usually WhatsApp exports or Canva downloads uploaded directly)

---

## Phase C: Script and third-party audit

From PageSpeed, extract:
- Third-party script domains and their transfer size
- Total script count

**Questions to answer:**
- Are there duplicate analytics/pixel scripts? (e.g. Meta pixel loaded twice)
- Are loyalty/rewards scripts loading on every page or only when needed?
- Is the checkout tool preloading on the homepage? (Unnecessary if not needed until cart)

**Common findings:**
- `bonb_rewards_overhead` — loyalty script loads on every page, adding weight to pages where it's irrelevant
- `shopflo_checkout_preload` — checkout JS preloads on homepage, blocking render for non-checkout pages
- `judgeme_css_split` — review app loads multiple CSS files as separate requests instead of single bundled request

---

## Phase D: Checkout technical review

Check the checkout flow for:

**Payment tracking:**
- Does the checkout tool (Shopflo / Shopify Payments / other) send purchase events correctly?
- Query Shopflo analytics (if MCP connected): purchase event match rate vs Shopify orders

**Trust signals in checkout:**
- Trust badges displayed? (Secure payment, SSL, brand logos)
- If Shopflo: Shopflo Dashboard → Checkout Settings → Trust Badges → enabled?

**Order summary:**
- Is the order summary visible by default or collapsed?
- Collapsed order summary creates anxiety — customers want to confirm what they're buying before paying

**OTP / phone verification:**
- If checkout requires phone OTP before payment: note this as an abandonment risk
- Users who enter phone number but don't complete OTP are captured by the checkout tool but not by Shopify's abandoned checkout system — this creates an analytics gap
- Check if checkout tool has its own abandonment recovery for OTP-stage dropoffs

**Branding:**
- Does the checkout page match the store's brand?
- Mismatched checkout (generic Shopify/third-party styling) creates trust anxiety

**ACR (Abandoned Checkout Recovery):**
- Is the checkout tool's ACR/re-engagement module enabled?
- If yes: what's the recovery rate?
- If no: flag as P0 (combined with Audit 6 abandonment findings)

---

## Phase E: JavaScript error check

Browse the store as a visitor and check browser console for errors on:
- Homepage
- A product page
- The cart
- The checkout (first step)

If browser MCP is available, check for:
- JavaScript errors (red entries in console)
- Failed network requests (404s, 500s)
- Failed third-party script loads

**Flag any JavaScript error that occurs on a page with >1,000 sessions/month.**

---

## Output format

For each finding:

```
FINDING: [issue_id]
Page: homepage / pdp / checkout / site-wide
Priority: P0 / P1 / P2
Type: speed / script / checkout / js_error
Evidence: [PageSpeed score, specific metric, specific error message]
Impact: [estimated conversion or revenue impact]
Effort: [honest time estimate]
Fix steps: [numbered, specific]
```

**Update `data/issue_statuses.json`** with any new issues found.

---

## Common issues and IDs

| Issue | ID |
|-------|-----|
| Mobile speed score < 50 | `mobile_score_low` |
| >20% images not WebP | `images_not_webp` |
| Slow PDP render (> 4s LCP) | `pdp_slow_render` |
| JudgeMe loading multiple CSS files | `judgeme_css_split` |
| Loyalty rewards script on all pages | `bonb_rewards_overhead` |
| Checkout preloading on homepage | `shopflo_checkout_preload` |
| Script count > 80 | `script_count_high` |
| Shopflo payment tracking not firing | `shopflo_payment_tracking_broken` |
| JS errors on product cards | `moments_card_js_errors` |
| OTP wall causing invisible abandonments | `shopflo_otp_wall` |
| Trust badges disabled in checkout | `shopflo_trust_badges_off` |
| Order summary collapsed by default | `shopflo_order_summary_collapsed` |
| Checkout branding not matching store | `shopflo_branding_missing` |
| ACR re-engagement module not enabled | `shopflo_acr_survey_missing` |
