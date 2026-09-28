-- ============================================================
-- 01_schema.sql
-- Creates the kirana_analytics database and all tables
-- ============================================================

CREATE DATABASE IF NOT EXISTS kirana_analytics;
USE kirana_analytics;

DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS suppliers;

-- ------------------------------------------------------------
-- SUPPLIERS
-- ------------------------------------------------------------
CREATE TABLE suppliers (
    supplier_id       VARCHAR(10) PRIMARY KEY,
    supplier_name     VARCHAR(100) NOT NULL,
    supplier_location VARCHAR(50),
    lead_time_days    INT NOT NULL,
    supplier_rating   DECIMAL(2,1)
);

-- ------------------------------------------------------------
-- CUSTOMERS
-- ------------------------------------------------------------
CREATE TABLE customers (
    customer_id       VARCHAR(10) PRIMARY KEY,
    customer_name     VARCHAR(100) NOT NULL,
    gender            VARCHAR(10),
    age               INT,
    city              VARCHAR(50),
    customer_segment  VARCHAR(20),
    registration_date DATE
);

-- ------------------------------------------------------------
-- PRODUCTS
-- ------------------------------------------------------------
CREATE TABLE products (
    product_id      VARCHAR(10) PRIMARY KEY,
    product_name    VARCHAR(150) NOT NULL,
    category        VARCHAR(50),
    sub_category    VARCHAR(50),
    brand           VARCHAR(50),
    unit            VARCHAR(20),
    cost_price      DECIMAL(10,2) NOT NULL,
    selling_price   DECIMAL(10,2) NOT NULL,
    supplier_id     VARCHAR(10),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

-- ------------------------------------------------------------
-- SALES
-- ------------------------------------------------------------
CREATE TABLE sales (
    sale_id         VARCHAR(10) PRIMARY KEY,
    sale_date       DATE NOT NULL,
    customer_id     VARCHAR(10),
    product_id      VARCHAR(10),
    quantity        INT NOT NULL,
    discount        DECIMAL(5,2) DEFAULT 0,
    payment_method  VARCHAR(20),
    store_location  VARCHAR(50),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    INDEX idx_sale_date (sale_date),
    INDEX idx_product (product_id),
    INDEX idx_customer (customer_id)
);

-- ------------------------------------------------------------
-- INVENTORY
-- ------------------------------------------------------------
CREATE TABLE inventory (
    inventory_date    DATE NOT NULL,
    product_id        VARCHAR(10),
    opening_stock     INT,
    received_stock    INT,
    sold_quantity     INT,
    closing_stock     INT,
    damaged_quantity  INT,
    PRIMARY KEY (inventory_date, product_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
