-- ============================================================
-- 03_analysis_queries.sql
-- Business analysis queries: beginner -> advanced
-- ============================================================
USE kirana_analytics;

-- ============================================================
-- BEGINNER: SELECT, WHERE, ORDER BY, GROUP BY, HAVING, aggregates
-- ============================================================

-- Q1. Total revenue
-- What it does: sums (qty * price * (1-discount)) across all sales.
-- Why useful: single top-line KPI for the whole business.
-- Output columns: total_revenue
-- Interview point: revenue must account for discounts, not just price*qty.
SELECT ROUND(SUM(s.quantity * p.selling_price * (1 - s.discount/100)), 2) AS total_revenue
FROM sales s
JOIN products p ON s.product_id = p.product_id;

-- Q2. Total profit
-- What it does: revenue minus cost across all sales.
-- Why useful: shows real profitability, not just sales volume.
-- Output columns: total_profit
SELECT ROUND(SUM(s.quantity * (p.selling_price*(1-s.discount/100) - p.cost_price)), 2) AS total_profit
FROM sales s
JOIN products p ON s.product_id = p.product_id;

-- Q3. Monthly revenue
-- What it does: groups revenue by calendar month.
-- Why useful: reveals seasonality and growth trend.
-- Output columns: month, monthly_revenue
SELECT DATE_FORMAT(s.sale_date, '%Y-%m') AS month,
       ROUND(SUM(s.quantity * p.selling_price * (1 - s.discount/100)), 2) AS monthly_revenue
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY month
ORDER BY month;

-- Q4. Monthly profit
-- Same as Q3 but profit-based.
SELECT DATE_FORMAT(s.sale_date, '%Y-%m') AS month,
       ROUND(SUM(s.quantity * (p.selling_price*(1-s.discount/100) - p.cost_price)), 2) AS monthly_profit
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY month
ORDER BY month;

-- Q5. Top 10 products by revenue
-- Why useful: identifies best-sellers to prioritize stocking.
SELECT p.product_id, p.product_name,
       ROUND(SUM(s.quantity * p.selling_price * (1 - s.discount/100)), 2) AS revenue
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY revenue DESC
LIMIT 10;

-- Q6. Slow-moving products (bottom 10 by quantity sold)
-- Why useful: flags candidates for discontinuation or promotion.
SELECT p.product_id, p.product_name, SUM(s.quantity) AS total_qty_sold
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.product_id, p.product_name
HAVING total_qty_sold > 0
ORDER BY total_qty_sold ASC
LIMIT 10;

-- Q7. Category performance
-- Why useful: shows which category drives revenue/profit.
SELECT p.category,
       ROUND(SUM(s.quantity * p.selling_price * (1 - s.discount/100)), 2) AS revenue,
       ROUND(SUM(s.quantity * (p.selling_price*(1-s.discount/100) - p.cost_price)), 2) AS profit
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC;

-- Q8. Highest-margin products (%)
-- Why useful: distinguishes "high revenue" from "high margin" products.
SELECT product_id, product_name, category,
       ROUND(((selling_price - cost_price) / selling_price) * 100, 2) AS margin_pct
FROM products
ORDER BY margin_pct DESC
LIMIT 10;

-- ============================================================
-- INTERMEDIATE: JOIN, LEFT JOIN, CASE, subqueries, date functions
-- ============================================================

-- Q9. Top customers by spend
SELECT c.customer_id, c.customer_name,
       ROUND(SUM(s.quantity * p.selling_price * (1 - s.discount/100)), 2) AS total_spend
FROM sales s
JOIN customers c ON s.customer_id = c.customer_id
JOIN products p ON s.product_id = p.product_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_spend DESC
LIMIT 10;

-- Q10. Repeat customers (more than 1 distinct purchase date)
-- Why useful: repeat customers = loyalty, valuable for retention strategy.
SELECT customer_id, COUNT(DISTINCT sale_date) AS visit_days
FROM sales
GROUP BY customer_id
HAVING visit_days > 1
ORDER BY visit_days DESC;

-- Q11. Customer segments — revenue contribution
SELECT c.customer_segment,
       COUNT(DISTINCT c.customer_id) AS customers,
       ROUND(SUM(s.quantity * p.selling_price * (1 - s.discount/100)), 2) AS revenue
FROM sales s
JOIN customers c ON s.customer_id = c.customer_id
JOIN products p ON s.product_id = p.product_id
GROUP BY c.customer_segment
ORDER BY revenue DESC;

-- Q12. Payment method analysis
SELECT payment_method,
       COUNT(*) AS num_transactions,
       ROUND(SUM(quantity), 0) AS total_qty
FROM sales
WHERE payment_method IS NOT NULL
GROUP BY payment_method
ORDER BY num_transactions DESC;

-- Q13. Inventory status (latest snapshot per product) using a subquery
SELECT i.product_id, p.product_name, i.closing_stock, i.inventory_date
FROM inventory i
JOIN products p ON i.product_id = p.product_id
WHERE i.inventory_date = (
    SELECT MAX(inventory_date) FROM inventory
)
ORDER BY i.closing_stock ASC;

-- Q14. Stockout products (closing stock = 0 on latest date)
SELECT i.product_id, p.product_name
FROM inventory i
JOIN products p ON i.product_id = p.product_id
WHERE i.inventory_date = (SELECT MAX(inventory_date) FROM inventory)
  AND i.closing_stock = 0;

-- Q15. Reorder candidates using CASE (simple threshold logic)
SELECT i.product_id, p.product_name, i.closing_stock,
       CASE
           WHEN i.closing_stock = 0 THEN 'REORDER NOW'
           WHEN i.closing_stock < 20 THEN 'LOW STOCK'
           WHEN i.closing_stock > 250 THEN 'OVERSTOCK'
           ELSE 'HEALTHY'
       END AS stock_status
FROM inventory i
JOIN products p ON i.product_id = p.product_id
WHERE i.inventory_date = (SELECT MAX(inventory_date) FROM inventory)
ORDER BY i.closing_stock ASC;

-- ============================================================
-- ADVANCED: CTEs, RANK/DENSE_RANK, LAG/LEAD, SUM() OVER(), running totals
-- ============================================================

-- Q16. Month-over-month sales growth %
WITH monthly AS (
    SELECT DATE_FORMAT(s.sale_date, '%Y-%m') AS month,
           SUM(s.quantity * p.selling_price * (1 - s.discount/100)) AS revenue
    FROM sales s
    JOIN products p ON s.product_id = p.product_id
    GROUP BY month
)
SELECT month, ROUND(revenue,2) AS revenue,
       ROUND(LAG(revenue) OVER (ORDER BY month), 2) AS prev_month_revenue,
       ROUND(((revenue - LAG(revenue) OVER (ORDER BY month)) / LAG(revenue) OVER (ORDER BY month)) * 100, 2) AS mom_growth_pct
FROM monthly
ORDER BY month;

-- Customer ranking by spend (RANK vs DENSE_RANK)
-- Interview point: RANK() skips numbers after ties; DENSE_RANK() does not.
WITH customer_spend AS (
    SELECT c.customer_id, c.customer_name,
           SUM(s.quantity * p.selling_price * (1 - s.discount/100)) AS total_spend
    FROM sales s
    JOIN customers c ON s.customer_id = c.customer_id
    JOIN products p ON s.product_id = p.product_id
    GROUP BY c.customer_id, c.customer_name
)
SELECT customer_id, customer_name, ROUND(total_spend,2) AS total_spend,
       RANK()       OVER (ORDER BY total_spend DESC) AS rank_std,
       DENSE_RANK() OVER (ORDER BY total_spend DESC) AS dense_rank_std
FROM customer_spend
ORDER BY total_spend DESC
LIMIT 20;

-- Product ranking by revenue within each category
WITH product_rev AS (
    SELECT p.category, p.product_id, p.product_name,
           SUM(s.quantity * p.selling_price * (1 - s.discount/100)) AS revenue
    FROM sales s
    JOIN products p ON s.product_id = p.product_id
    GROUP BY p.category, p.product_id, p.product_name
)
SELECT category, product_id, product_name, ROUND(revenue,2) AS revenue,
       RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS rank_in_category
FROM product_rev
ORDER BY category, rank_in_category;

-- Running total of daily revenue (SUM() OVER, running totals)
WITH daily AS (
    SELECT s.sale_date,
           SUM(s.quantity * p.selling_price * (1 - s.discount/100)) AS daily_revenue
    FROM sales s
    JOIN products p ON s.product_id = p.product_id
    GROUP BY s.sale_date
)
SELECT sale_date, ROUND(daily_revenue,2) AS daily_revenue,
       ROUND(SUM(daily_revenue) OVER (ORDER BY sale_date), 2) AS running_total_revenue
FROM daily
ORDER BY sale_date;

-- LEAD example: next month's revenue compared to current
WITH monthly AS (
    SELECT DATE_FORMAT(s.sale_date, '%Y-%m') AS month,
           SUM(s.quantity * p.selling_price * (1 - s.discount/100)) AS revenue
    FROM sales s
    JOIN products p ON s.product_id = p.product_id
    GROUP BY month
)
SELECT month, ROUND(revenue,2) AS revenue,
       ROUND(LEAD(revenue) OVER (ORDER BY month), 2) AS next_month_revenue
FROM monthly
ORDER BY month;
