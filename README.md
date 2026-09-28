# Smart Kirana Store Intelligence & Demand Analytics

**Suggested repo name:** `smart-kirana-demand-analytics`

## Overview
An end-to-end Data Analyst portfolio project that turns a local kirana (grocery)
store's raw sales, customer, product, inventory, and supplier data into a
decision-ready analytics system — covering sales trends, profitability,
customer behavior, inventory health, and a demand-driven reorder system.

## Business Problem
A kirana store owner has data scattered across systems with no centralized
view. The project answers: **"What should the store manager sell, stock,
reorder, and investigate?"**

## Objectives
- Quantify revenue, profit, and margin trends
- Identify best-selling and slow-moving products
- Understand customer segments and repeat-purchase behavior
- Monitor inventory health and flag stockout risk
- Recommend what and how much to reorder, using an explainable formula
- Present all of the above in an interactive Power BI dashboard

## Features
- Synthetic but realistic dataset (1,200 customers, 80 products, ~55,000 transactions)
- Intentional data-quality issues for a genuine Excel cleaning exercise
- Full MySQL schema with beginner → advanced SQL (joins, CTEs, window functions)
- Python pipeline: cleaning, EDA, feature engineering, demand analysis, reorder logic
- Explainable moving-average demand forecast
- Reorder Point formula-based Smart Reorder System
- 6-page Power BI dashboard with 15 DAX measures (including the loyal customer metric)
- Reconciled totals across SQL, Python, and Power BI

## Architecture
```
Python (generate) → Raw CSVs
   → Excel (inspect/clean/validate)
   → MySQL (structured storage + SQL analysis)
   → Python (EDA, profit/margin, demand, forecast, reorder logic)
   → Final CSVs (star schema)
   → Power BI (data model, DAX, dashboard)
   → Business Insights → GitHub → Resume → Interview
```

## Dataset
| File | Rows | Description |
|---|---|---|
| `customers.csv` | 1,200 | Customer demographics & segment |
| `products.csv` | 80 | Product catalog, cost/selling price |
| `sales.csv` | 55,000 | Clean transaction-level sales |
| `raw_sales.csv` | 55,150 | Same data + intentional quality issues (for Excel exercise) |
| `inventory.csv` | 29,280 | Daily stock movement per product |
| `suppliers.csv` | 15 | Supplier lead time & rating |

### Data Dictionary (key fields)
- **Primary keys:** `customer_id`, `product_id`, `sale_id`, `supplier_id`, (`inventory_date`+`product_id`)
- **Foreign keys:** `sales.customer_id → customers`, `sales.product_id → products`, `products.supplier_id → suppliers`, `inventory.product_id → products`
- **Intentional data quality issues (raw_sales.csv only):** ~150 duplicate rows, ~200 missing `payment_method`, inconsistent casing/whitespace in `store_location`, ~25 negative quantities, ~15 invalid discounts (>100%)

## Excel Process
Open the workbook at [`excel/Kirana_Analytics.xlsx`](excel/Kirana_Analytics.xlsx) — this is the cleaned Excel deliverable for the data preparation and validation stage.

> GitHub does not render Excel files inline in the browser; it downloads them for viewing. The workbook is included in the repo so recruiters can open it locally.

## SQL Process
See [`sql/01_schema.sql`](sql/01_schema.sql), [`sql/02_import_data.sql`](sql/02_import_data.sql),
[`sql/03_analysis_queries.sql`](sql/03_analysis_queries.sql) — 16 business questions from
beginner SELECTs to CTEs, RANK/DENSE_RANK, LAG/LEAD, and running totals.

## Python Process
Seven scripts in `python/`, run in order:
```
00_generate_dataset.py
01_data_validation.py
02_data_cleaning.py
03_eda.py
04_feature_engineering.py
05_demand_analysis.py
06_reorder_recommendation.py
07_export_final_tables.py
```

### Smart Reorder System
```
Safety Stock   = Average Daily Demand x 3 days
Reorder Point  = (Average Daily Demand x Supplier Lead Time) + Safety Stock
Stock Status   = REORDER NOW / LOW STOCK / HEALTHY / OVERSTOCK
```
Forecast demand uses a **14-day moving average** — simple, explainable, and
appropriate for an MVP with one year of seasonally-noisy data (see
`python/05_demand_analysis.py` for the full rationale).

## Power BI Process
Open the dashboard file at [`powerbi/kirana_Analytics.pbix`](powerbi/kirana_Analytics.pbix) — this contains the star schema model, 15 DAX measures, and the 6-page dashboard.

> Note: The Top Customers visual in Power BI groups by `customer_name`, not `customer_id`. Because customer names repeat across IDs, this table will not match SQL totals exactly. The SQL output using `customer_id` is the reliable source for customer-level analysis.

## Dashboard Screenshots

![Executive Overview](powerbi/screenshots/Executive%20Overview.png)
![Sales Analytics](powerbi/screenshots/Sales%20Analytics.png)
![Customer Analytics](powerbi/screenshots/Customer%20Analytics.png)
![Inventory Intelligence](powerbi/screenshots/Inventory%20Intelligence.png)
![Product Profitability](powerbi/screenshots/Product%20Profitability.png)
![Demand & Reorder](powerbi/screenshots/Demand%20%26%20Reorder.png)

## Key Insights
Highlights from the project:
- All 1,200 customers are repeat buyers under the project definition (they appear on multiple purchase days), and customer names repeat across multiple customer IDs in the source data.
- Household, Dairy, and Personal Care categories drive over half of total revenue.
- 17 of 80 products are currently at REORDER NOW status, with dairy items over-represented.
- Some high-revenue staple products (wheat flour, onion, cooking oil) carry unusually low margins.
- The Top Customers table in Power BI is name-based, so its totals are directional rather than the authoritative SQL view.

A visual summary of the analysis is available in [`docs/charts`](docs/charts/).

## Business Recommendations
1. Shorten dairy restocking cycles to reduce stockouts.
2. Rebalance the 33 overstocked SKUs to free up working capital.
3. Revisit supplier pricing on high-revenue, low-margin staples.

## Tech Stack
Excel · MySQL · Python (Pandas, NumPy, Matplotlib, Seaborn) · Power BI · DAX

## Project Structure
```
kirana-analytics/
├── data/              # raw, cleaned & final CSVs
│   └── final/         # star-schema tables for Power BI
├── excel/             # Kirana_Analytics.xlsx
├── sql/               # schema, import, analysis queries
├── python/            # data pipeline scripts
├── powerbi/           # .pbix dashboard + screenshots
├── docs/charts/       # project charts and visual summaries
├── README.md
├── .gitignore
├── requirements.txt
└── .git/
```

## How to Run
```bash
pip install -r requirements.txt
cd python
python 00_generate_dataset.py
python 01_data_validation.py
python 02_data_cleaning.py
python 03_eda.py
python 04_feature_engineering.py
python 05_demand_analysis.py
python 06_reorder_recommendation.py
python 07_export_final_tables.py
```
Then import `data/final/*.csv` into MySQL (see `sql/`) and open the dashboard in [`powerbi/kirana_Analytics.pbix`](powerbi/kirana_Analytics.pbix).

## Future Improvements
- Replace moving-average forecast with a seasonal model (e.g., Holt-Winters) as data volume grows
- Automate the Power BI refresh via a scheduled pipeline
- Add a supplier performance scorecard (on-time delivery rate)
- Extend to multi-store comparison if the business expands
