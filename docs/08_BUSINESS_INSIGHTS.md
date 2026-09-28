# Part 8 — Business Insights (from executed project data)

*All numbers below are computed from the actual generated dataset by running the
Python pipeline (`sales_enriched.csv` and `reorder_recommendations.csv`). Re-run
the scripts after any data change and refresh these numbers.*

## Headline numbers
- **Total Revenue:** ₹76,07,051
- **Total Profit:** ₹13,09,678 (≈17.2% overall margin)
- **Total Orders:** 54,960
- **Total Customers:** 1,200

## Sales insights
1. Household products contribute the largest revenue share at 20.8%, followed by Dairy (17.2%) and Personal Care (16.1%).
2. Revenue dips noticeably in June and spikes sharply in October–November, consistent with a festive-season demand pattern.
3. Weekend sales (Saturday/Sunday) run higher than weekday sales, reflecting typical kirana shopping behavior.
4. Bakery and Vegetables are the smallest revenue categories (5.8% and 7.1% respectively) — likely due to lower price points rather than low demand.
5. UPI is the dominant payment method, ahead of Cash, Card, and Wallet — reflecting the shift toward digital payments.

## Customer insights
1. "Regular" segment customers drive 54% of total revenue despite being less than half the customer base.
2. "Premium" segment contributes 30.4% of revenue from a smaller customer count — high value per customer.
3. "New" customers contribute only 2.7% of revenue, as expected for recently acquired customers.
4. All 1,200 customers are repeat buyers by the project definition (they visit on multiple distinct purchase days). The project also tracks a 10+ visits loyalty metric to separate frequent shoppers from the broader customer base.
5. Customer spend is concentrated: the top 10 customers by spend materially outweigh an average customer's spend (see SQL Q9).

## Inventory insights
1. Of 80 products, 17 are currently in **REORDER NOW** status (zero stock) — including HUL Paneer and Local Brand Curd, both perishable dairy items needing urgent restocking.
2. 24 products are in **LOW STOCK** status, approaching their reorder point.
3. 33 products are **OVERSTOCK** — capital tied up in excess inventory that could be reallocated.
4. Only 6 products are currently at a **HEALTHY** stock level — a signal to review reorder point assumptions or restocking cadence for the rest.
5. Dairy products (Paneer, Curd) appear disproportionately in the REORDER NOW list, consistent with their short shelf life and high turnover.

## Profitability insights
1. Aashirvaad-branded products dominate the top-5 revenue list, led by Aashirvaad Soap and Aashirvaad Detergent.
2. Aashirvaad Wheat Flour is a high-revenue product (₹3.34L) but has one of the lowest profit margins (~5.7%) — a high-revenue/low-margin product worth renegotiating supplier terms on.
3. HUL Onion and Dabur Cooking Oil show a similar high-revenue/low-margin pattern (~6.4–6.7% margin), typical of staple/commodity items.
4. Personal Care and Household categories carry higher margins by design (35% and 30% target margins respectively) and are worth promoting more actively.
5. Grocery and Vegetables, while high in volume, are lower-margin categories — profitable mainly through volume, not markup.

## Business recommendations
1. **Prioritize dairy restocking**: shorten the reorder cycle or negotiate a shorter lead time with dairy suppliers, since Paneer and Curd repeatedly hit zero stock.
2. **Rebalance overstocked inventory**: 33 products are overstocked, tying up working capital — reduce next restock quantity for these SKUs and consider promotional pricing to move slow stock.
3. **Protect margin on staple items**: for high-revenue/low-margin products like Wheat Flour, Onion, and Cooking Oil, explore bulk-purchase supplier discounts or a small price adjustment, since these drive volume but contribute little profit.

*(Re-run `python 05_demand_analysis.py` and `06_reorder_recommendation.py` after any
new inventory snapshot to refresh the reorder-status counts above.)*
