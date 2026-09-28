-- ============================================================
-- 02_import_data.sql
-- Loads CSVs into MySQL tables (order matters: parents before children)
-- ============================================================
-- NOTE:
-- 1) Run this script from the project root (kirana_project/) or adjust the
--    paths below to your local MySQL working directory.
-- 2) MySQL must have 'secure_file_priv' allowing the path, OR run the mysql
--    client with --local-infile=1 and use LOAD DATA LOCAL INFILE.
-- 3) Use repo-relative paths so anyone can clone the project without editing
--    machine-specific usernames or absolute file system paths.
-- 4) On Windows, forward slashes are accepted in MySQL paths and are kept
--    consistent with a GitHub-friendly project layout.

USE kirana_analytics;

SET FOREIGN_KEY_CHECKS = 0;
LOAD DATA LOCAL INFILE 'data/suppliers.csv'
INTO TABLE suppliers
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(supplier_id, supplier_name, supplier_location, lead_time_days, supplier_rating);

LOAD DATA LOCAL INFILE 'data/customers.csv'
INTO TABLE customers
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(customer_id, customer_name, gender, age, city, customer_segment, registration_date);

LOAD DATA LOCAL INFILE 'data/products.csv'
INTO TABLE products
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(product_id, product_name, category, sub_category, brand, unit, cost_price, selling_price, supplier_id);

LOAD DATA LOCAL INFILE 'data/sales.csv'
INTO TABLE sales
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(sale_id, sale_date, customer_id, product_id, quantity, discount, payment_method, store_location);

LOAD DATA LOCAL INFILE 'data/inventory.csv'
INTO TABLE inventory
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(inventory_date, product_id, opening_stock, received_stock, sold_quantity, closing_stock, damaged_quantity);

SET FOREIGN_KEY_CHECKS = 1;

-- ------------------------------------------------------------
-- VERIFY ROW COUNTS
-- ------------------------------------------------------------
SELECT 'suppliers' AS table_name, COUNT(*) AS row_count FROM suppliers
UNION ALL
SELECT 'customers', COUNT(*) FROM customers
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'sales', COUNT(*) FROM sales
UNION ALL
SELECT 'inventory', COUNT(*) FROM inventory;

-- ------------------------------------------------------------
-- DATA QUALITY CHECKS
-- ------------------------------------------------------------
-- Orphan sales (broken FK)
SELECT COUNT(*) AS orphan_sales_customers
FROM sales s LEFT JOIN customers c ON s.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

SELECT COUNT(*) AS orphan_sales_products
FROM sales s LEFT JOIN products p ON s.product_id = p.product_id
WHERE p.product_id IS NULL;

-- Negative or zero quantities
SELECT COUNT(*) AS invalid_quantities FROM sales WHERE quantity <= 0;

-- Invalid discounts
SELECT COUNT(*) AS invalid_discounts FROM sales WHERE discount < 0 OR discount > 100;

-- Duplicate sale_id
SELECT sale_id, COUNT(*) c FROM sales GROUP BY sale_id HAVING c > 1;
