# Audit 6 — Revenue & AOV

**Goal:** Find where revenue is leaking after a visitor becomes interested — abandoned checkouts, upsell gaps, retention failures, and AOV constraints. Calculate specific ₹ amounts for each opportunity using actual store data.

**Constraint:** Every ₹ estimate must come from actual data pulled in this audit. No industry benchmark presented as store-specific fact.

---

## Phase A: AOV analysis

Pull from Shopify MCP:

```sql
FROM orders
SELECT
  COUNT(*) as order_count,
  AVG(total_price) as avg_order_value,
  MIN(total_price) as min_order,
  MAX(total_price) as max_order,
  SUM(total_price) as total_revenue
WHERE date >= 30_days_ago
```

Also pull AOV distribution:
```sql
FROM orders
SELECT
  CASE
    WHEN total_price < 1000 THEN 'under_1000'
    WHEN total_price < 2500 THEN '1000_2500'
    WHEN total_price < 5000 THEN '2500_5000'
    WHEN total_price < 10000 THEN '5000_10000'
    WHEN total_price < 25000 THEN '10000_25000'
    ELSE 'above_25000'
  END as price_band,
  COUNT(*) as orders,
  SUM(total_price) as revenue
WHERE date >= 30_days_ago
GROUP BY price_band
```

**Questions to answer:**
- What is the blended AOV?
- If admin/WhatsApp orders dominate (from Audit 1): what is the D2C-only AOV vs admin/B2B AOV?
- What price band has the most orders? (This is the "typical" D2C customer)
- How many orders are in the ₹6K–₹10K range? (Near free-shipping threshold — upsell target)
- What is the free shipping threshold, and how many orders are just below it?

---

## Phase B: Cart abandonment recovery

**Step 1: Check current abandonment email status**

Shopify Admin → Marketing → Automations — is the abandoned checkout sequence enabled?

Also check: does the checkout tool (if not native Shopify) have its own abandonment recovery?

**Step 2: Pull abandonment data**

```graphql
{
  abandonedCheckouts(first: 50, sortKey: CREATED_AT, reverse: true) {
    edges {
      node {
        createdAt
        totalPriceV2 { amount }
        lineItems(first: 5) {
          edges { node { title quantity } }
        }
      }
    }
  }
}
```

Calculate:
- Number of abandoned checkouts in last 30 days
- Total value of abandoned checkouts in last 30 days
- Average abandoned checkout value

**Step 3: Identify OTP-wall invisible abandonments (if applicable)**

If the store uses a checkout tool with phone verification before payment (Shopflo, etc.):
- Shopify only captures abandonments after a cart is created
- Phone-capture-stage abandonments don't appear in Shopify's abandoned checkout data
- Estimate invisible abandonment: `(sessions × checkout_entry_rate × otp_abandonment_rate) - shopify_reported_abandonments`

If Shopflo ACR data is available, compare Shopflo's abandonment count vs Shopify's count to size the gap.

**Recovery potential calculation:**
```
Monthly recovery potential = abandoned_checkout_value × 0.15  (conservative, 15% recovery rate)
Monthly recovery potential = abandoned_checkout_value × 0.20  (optimistic, 20% recovery rate)
```

---

## Phase C: Post-purchase upsell audit

**Check:**
- Is there a post-purchase upsell offer on the thank-you page?
- If using Shopflo: is the post-purchase upsell module enabled?

If no post-purchase upsell exists:

Calculate potential:
```
Monthly upsell potential = monthly_d2c_orders × take_rate × upsell_offer_value
```

Use take_rate = 0.10 (10% conservative) and 0.15 (15% optimistic).

Identify the best upsell offer by looking at: which products are frequently bought by the same customer on their second order? These are natural set completions.

---

## Phase D: Free shipping threshold nudge

**Pull threshold:** What is the current free shipping minimum?

**Pull orders near threshold:**
```sql
FROM orders
WHERE total_price BETWEEN (threshold × 0.6) AND threshold
  AND date >= 30_days_ago
SELECT COUNT(*), AVG(total_price), SUM(total_price)
```

**Calculate:** If 30% of these orders were nudged to the threshold:
```
lift_revenue = orders_near_threshold × 0.30 × (threshold - avg_order_in_band)
```

**Check:** Is there a free shipping progress bar in the cart?

---

## Phase E: Gift add-ons

**For gifting-positioned stores:**

- Is there a gift wrapping option at PDP or checkout?
- Is there a gift message option?
- Is there a gift box / premium packaging SKU?

Calculate potential:
```
gift_wrap_potential = monthly_orders × 0.25 × gift_wrap_price
```

Use 25% as conservative attach rate for gifting-positioned brands.

---

## Phase F: Repeat purchase rate

Pull from Shopify MCP:
```sql
FROM customers
SELECT
  COUNT(*) as total_customers,
  SUM(CASE WHEN orders_count > 1 THEN 1 ELSE 0 END) as repeat_customers,
  AVG(orders_count) as avg_orders_per_customer,
  AVG(total_spent) as avg_ltv
WHERE date >= 90_days_ago
```

**Questions to answer:**
- What % of customers have placed more than 1 order?
- What is the average time between first and second order? (This = optimal re-engagement window)
- Is there a post-purchase email/WhatsApp sequence running?

**Flag if:** Repeat purchase rate < 15% with no automated post-purchase sequence in place. This is a retention gap.

---

## Phase G: Product performance

Pull top and bottom performers:
```sql
FROM sales
SELECT product_title, SUM(net_sales) as revenue, SUM(quantity) as units, COUNT(DISTINCT order_id) as orders
WHERE date >= 30_days_ago
GROUP BY product_title
ORDER BY revenue DESC
LIMIT 20
```

**Questions to answer:**
- What are the top 3 products by revenue?
- What are the top 3 products by order count?
- Are there any products with significant traffic but near-zero revenue? (Content or pricing issue)
- Is there a price point gap? (e.g. nothing in the ₹500–₹1,500 range for entry-level customers)

---

## Phase H: Discount and coupon usage

Pull discount data:
```sql
FROM orders
WHERE discount_codes IS NOT NULL
  AND date >= 30_days_ago
SELECT COUNT(*) as discounted_orders, AVG(discount_amount) as avg_discount, SUM(discount_amount) as total_discount_given
```

**Questions to answer:**
- What % of orders use a discount code?
- What is the average discount amount vs AOV? (Discounts eating margin)
- Are customers who use discounts more or less likely to repeat purchase? (Discount addiction risk)

---

## Output format

For each finding:

```
FINDING: [issue_id]
Category: AOV / Abandonment / Retention / Product / Pricing
Priority: P0 / P1 / P2
Evidence: [specific numbers from this store's data]
Calculation: [show the working — e.g. "20 abandonments × ₹19,700 avg × 15% recovery = ₹59,100/month"]
Impact: [₹ range per month]
Effort: [honest time estimate]
Fix steps: [numbered, specific]
```

**Update `data/issue_statuses.json`** with any new issues found.

---

## Common issues and IDs

| Issue | ID |
|-------|-----|
| No abandoned checkout email sequence | `no_abandonment_email_sequence` |
| No WhatsApp abandonment recovery | `no_whatsapp_abandonment_recovery` |
| OTP-wall invisible abandonments | `shopflo_otp_wall` (cross-ref Audit 3) |
| No free shipping threshold nudge in cart | `no_free_shipping_threshold_nudge` |
| No gift wrapping / add-on SKU | `no_gift_wrap_sku` |
| No post-purchase upsell | `no_post_purchase_upsell` |
| No post-purchase nurture sequence | `no_post_purchase_nurture_sequence` |
| Variant selector hiding purchase intent | `[product]_occasion_variants_hidden` |
| Price gap at low end | `no_entry_price_point_under_[amount]` |
