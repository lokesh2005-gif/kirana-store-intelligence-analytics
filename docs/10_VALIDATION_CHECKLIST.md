# Part 10 — Validation & Quality Checklist

## Data
- [x] No broken foreign keys (verified: sales.customer_id, sales.product_id, products.supplier_id all resolve)
- [x] Duplicates only in `raw_sales.csv` (intentional), none in clean tables
- [x] All dates parse validly (`sale_date`, `inventory_date`)
- [x] Prices are positive (`cost_price`, `selling_price` > 0)
- [x] Quantities are positive after cleaning
- [x] Inventory math is consistent: `closing_stock = opening_stock + received_stock - sold_quantity - damaged_quantity` (clamped at 0)

## SQL
- [ ] Run `sql/01_schema.sql`, confirm all 5 tables created without error
- [ ] Run `sql/02_import_data.sql`, confirm row counts match: customers=1200, products=80, sales=55000, inventory=29280, suppliers=15
- [ ] Run each query in `sql/03_analysis_queries.sql`, confirm no errors
- [ ] Compare `SELECT SUM(...)` total revenue against Python's `sales_enriched['revenue'].sum()` — should match to the rupee

## Python
- [x] All 8 scripts run without errors end-to-end (verified during build)
- [x] `cleaned_sales.csv` has fewer rows than `raw_sales.csv` (185 removed: duplicates + invalid rows)
- [x] `reorder_recommendations.csv` contains all 4 stock statuses (not just one)
- [x] Exported CSVs in `data/final/` have expected row counts

## Power BI
- [ ] All relationships show as active (no dashed/inactive lines) in Model view
- [ ] Slicers filter every visual on the page as expected
- [ ] DAX measures return non-blank values when no filter is applied
- [ ] Total Revenue card matches the SQL and Python total (reconciliation check)

## Business
- [x] All insights in `docs/08_BUSINESS_INSIGHTS.md` are backed by actual computed numbers, not placeholders
- [x] Recommendations are traceable to a specific metric (e.g., "17 products at REORDER NOW")
