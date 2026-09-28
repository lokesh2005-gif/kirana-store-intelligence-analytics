# Part 12 — Resume Bullets

- Built an end-to-end retail analytics pipeline (Excel, MySQL, Python/Pandas, Power BI) processing 55,000+ transactions across 80 products and 1,200 customers, including data cleaning, EDA, and a star-schema data model.
- Designed and implemented an explainable demand-forecasting and reorder-recommendation system in Python using moving averages and reorder-point logic, flagging stockout and overstock risk across the product catalog.
- Authored 15+ SQL queries spanning joins, CTEs, and window functions (RANK, LAG/LEAD, running totals) to analyze revenue, profit margin, and customer segments, then visualized results in a 6-page interactive Power BI dashboard with 14 DAX measures.

*(No percentages, accuracy figures, or business-impact claims are included beyond
what the executed project actually measured — update bullets only with real
numbers from your own run if you want to cite specifics.)*

---

# Part 13 — Interview Preparation

## 2-minute explanation
"I built an end-to-end analytics project for a fictional kirana store that had
sales, customer, product, inventory, and supplier data but no centralized way
to analyze it. I generated a realistic synthetic dataset — about 55,000
transactions across 80 products and 1,200 customers — with intentional data
quality issues so I could demonstrate real cleaning work.

I started in Excel to inspect and validate the raw data — checking for
duplicates, missing values, and invalid entries. Then I loaded the cleaned
data into MySQL, where I wrote SQL ranging from basic aggregations to window
functions like RANK and LAG to analyze revenue trends and customer behavior.

The core analysis is in Python — I calculated profit and margin, ran EDA to
find seasonal patterns, then built a demand forecast using a 14-day moving
average, which is simple and explainable for a business stakeholder. On top
of that, I built a reorder recommendation system using the classic
Reorder Point formula: average daily demand times lead time, plus safety
stock. That flags every product as REORDER NOW, LOW STOCK, HEALTHY, or
OVERSTOCK.

Finally, I modeled everything in Power BI as a star schema and built a
6-page dashboard — executive overview, sales, customers, inventory, product
profitability, and demand/reorder — all driven by DAX measures, with the
totals reconciled back against my SQL and Python outputs.

The business value is that a store manager could open this dashboard and
immediately know what to stock, what to reorder, and which products are
quietly losing margin."

## Excel
- **Why Excel?** It's still the fastest way to eyeball raw data, catch obvious quality issues, and produce quick pivot summaries before committing to a database schema.
- **What cleaning did you perform?** Removed duplicates, standardized text casing/whitespace, flagged and handled missing payment methods, removed invalid quantities/discounts.
- **Which formulas/Pivots did you use?** `COUNTIFS`, `COUNTBLANK`, `TRIM`/`PROPER`, `VLOOKUP` for revenue/cost lookups; Pivot Tables for monthly revenue, category revenue, and top products.

## SQL
- **Why SQL?** Relational integrity (foreign keys) and set-based aggregation are more reliable and auditable than doing joins in a spreadsheet at this data volume.
- **Explain JOINs:** INNER JOIN returns only matching rows across tables; LEFT JOIN keeps all rows from the left table even without a match — I used LEFT JOIN to find orphaned foreign keys during data-quality checks.
- **Explain CTE:** A `WITH` clause that creates a named, reusable temporary result set for that query — makes multi-step logic (e.g., compute monthly revenue, then compare month over month) readable instead of nesting subqueries.
- **Explain window functions:** Functions like `RANK()` or `SUM() OVER()` that compute a value across a set of rows related to the current row, without collapsing the result into one row per group like `GROUP BY` does.
- **RANK vs DENSE_RANK:** `RANK()` skips subsequent rank numbers after a tie (1,1,3); `DENSE_RANK()` doesn't skip (1,1,2).
- **Explain MoM growth:** Use `LAG()` to pull the previous month's value into the current row, then compute `(current - previous) / previous`.

## Python
- **Why Pandas?** Vectorized operations make merging tables and computing derived columns (revenue, profit, margin) across tens of thousands of rows fast and readable.
- **What cleaning did you perform?** Same core issues as Excel, but scripted and reproducible — duplicate removal, missing-value handling, invalid-value filtering, date parsing.
- **Why forecasting?** To move from "what happened" to "what's likely to happen next," which is what makes the reorder recommendations proactive instead of reactive.
- **Why did you choose the forecasting method?** A moving average is transparent and easy to explain to a non-technical store owner, doesn't require training/tuning, and is appropriate given a single year of data with weekly and seasonal noise — a more complex model would risk overfitting without added business value at this stage.

## Power BI
- **Explain the data model:** A star schema — one central FactSales (and FactInventory) table connected to Dimension tables (Product, Customer, Supplier, Date) via 1-to-many relationships.
- **Explain star schema:** Fact tables hold measures (revenue, quantity); dimension tables hold descriptive attributes (category, segment) — this structure keeps the model simple and query performance fast.
- **Explain DAX:** Data Analysis Expressions — the formula language used for measures and calculated columns in Power BI, similar in spirit to Excel formulas but context-aware.
- **Calculated column vs measure:** A calculated column is computed once per row and stored in the model; a measure is computed dynamically based on the current filter/slicer context and isn't stored as row data.
- **Explain relationships:** Defined by matching key columns between tables (e.g., `product_id`), with a cardinality (1-to-many here) and a filter direction that determines how a slicer selection propagates.
- **Explain dashboard design:** Grouped by audience question — executives want KPIs and trends first; operations wants inventory/reorder detail — so I split those into separate pages rather than one overloaded page.

## Business
- **How do you identify a reorder product?** Compare current stock against the reorder point (average daily demand × lead time + safety stock); if current stock is at or below that point, it needs reordering.
- **How would you reduce stockouts?** Shorten the review cycle for fast-moving/perishable items, increase safety stock for products with more demand variability, and negotiate shorter lead times with suppliers for high-turnover SKUs.
- **How would you identify low-margin products?** Compare `(selling_price - cost_price) / selling_price` across products, then cross-reference with revenue — the interesting cases are high-revenue but low-margin, since they represent real profit leakage.
- **How would you improve this in production?** Replace the synthetic data with a live database connection, automate the Python pipeline on a schedule, add a proper time-series model as more historical data accumulates, and add alerting so stockout risk is pushed to the manager rather than requiring a dashboard check.
