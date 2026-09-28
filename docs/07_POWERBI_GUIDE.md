# Part 7 — Power BI Guide

## 1. Import data
Get Data → Text/CSV → import each file from `data/final/`:
`FactSales.csv`, `FactInventory.csv`, `DimProduct.csv`, `DimCustomer.csv`,
`DimSupplier.csv`, `DimDate.csv`, `reorder_recommendations.csv`

## 2. Data model (star schema)

```
DimDate ────┐
DimProduct ─┼──< FactSales >──── DimCustomer
DimSupplier─┘        |
                FactInventory
```

Relationships (all **1-to-many**, single direction from Dim → Fact):
- `DimDate[date]` (1) → `FactSales[sale_date]` (many)
- `DimDate[date]` (1) → `FactInventory[inventory_date]` (many)
- `DimProduct[product_id]` (1) → `FactSales[product_id]` (many)
- `DimProduct[product_id]` (1) → `FactInventory[product_id]` (many)
- `DimProduct[product_id]` (1) → `reorder_recommendations[product_id]` (many, or 1-to-1)
- `DimCustomer[customer_id]` (1) → `FactSales[customer_id]` (many)
- `DimSupplier[supplier_id]` (1) → `DimProduct[supplier_id]` (many)

Mark `DimDate` as a **Date Table** (Modeling → Mark as Date Table).

## 3. DAX Measures

Create a new Measures table (Modeling → New Table → `Measures = {1}`, hide the column) and add:

```dax
Total Revenue = SUM(FactSales[revenue])

Total Cost = SUM(FactSales[cost])

Total Profit = SUM(FactSales[profit])

Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0)

Total Orders = DISTINCTCOUNT(FactSales[sale_id])

Total Quantity = SUM(FactSales[quantity])

Total Customers = DISTINCTCOUNT(FactSales[customer_id])

Average Order Value = DIVIDE([Total Revenue], [Total Orders], 0)

Repeat Customers =
VAR CustomerVisits =
    SUMMARIZE(FactSales, FactSales[customer_id], "VisitDays", DISTINCTCOUNT(FactSales[sale_date]))
RETURN
    COUNTROWS(FILTER(CustomerVisits, [VisitDays] > 1))

Revenue MoM % =
VAR CurrentRevenue = [Total Revenue]
VAR PreviousRevenue = CALCULATE([Total Revenue], DATEADD(DimDate[date], -1, MONTH))
RETURN DIVIDE(CurrentRevenue - PreviousRevenue, PreviousRevenue, 0)

Profit MoM % =
VAR CurrentProfit = [Total Profit]
VAR PreviousProfit = CALCULATE([Total Profit], DATEADD(DimDate[date], -1, MONTH))
RETURN DIVIDE(CurrentProfit - PreviousProfit, PreviousProfit, 0)

Stockout Count =
CALCULATE(COUNTROWS(reorder_recommendations), reorder_recommendations[stock_status] = "REORDER NOW")

Low Stock Count =
CALCULATE(COUNTROWS(reorder_recommendations), reorder_recommendations[stock_status] = "LOW STOCK")

Reorder Count =
CALCULATE(COUNTROWS(reorder_recommendations),
    reorder_recommendations[stock_status] IN {"REORDER NOW", "LOW STOCK"})
```

**Calculated column vs measure (interview point):** a calculated column is computed
row-by-row and stored in the model (e.g., `Profit Margin % per row`); a measure is
computed on the fly based on filter context (e.g., total margin for whatever is
currently selected). Prefer measures for aggregations — smaller model, always
context-aware.

## 4. Dashboard pages

**Page 1 — Executive Overview**
KPI cards: Total Revenue, Total Profit, Total Orders, Total Customers, Profit Margin %.
Visuals: line chart (monthly revenue), line chart (monthly profit), bar chart (sales by category), bar chart (top 10 products), pie/donut (payment method split).

**Page 2 — Sales Analytics**
Line chart: daily/weekly/monthly sales (use a slicer to toggle granularity via DimDate hierarchy).
Bar charts: category sales, product sales. Column chart: discount analysis (avg discount by category).

**Page 3 — Customer Analytics**
Cards: Total Customers, Repeat Customers. Bar chart: customer segments by revenue.
Table: top customers. Histogram: purchase frequency distribution.

**Page 4 — Inventory Intelligence**
Cards: Stockout Count, Low Stock Count, Reorder Count. Table: current stock by product.
Bar chart: stock status distribution. Table: reorder recommendations, conditionally
formatted (red = REORDER NOW, orange = LOW STOCK, green = HEALTHY, blue = OVERSTOCK).

**Page 5 — Product Profitability** *(optional if time-constrained)*
Scatter chart: Revenue (x) vs Profit Margin % (y), bubble size = quantity — highlights
high-revenue/low-margin products in one view. Table: category profitability.

**Page 6 — Demand & Reorder** *(optional if time-constrained)*
Line chart: historical demand vs forecast demand per product (use a product slicer).
Table: reorder point, recommended order qty, stock status from `reorder_recommendations`.

## 5. Manual steps that can't be scripted
- Setting visual colors/conditional formatting: Format pane → Conditional formatting → Rules
- Creating slicers: Insert → Slicer, then bind to DimDate/DimProduct/Category
- Publishing to Power BI Service: File → Publish → select workspace

## 6. Reconciliation checkpoint
Total Revenue in Power BI **must equal** the SQL `SELECT SUM(...)` result (Q1) and the
Python `sales_enriched['revenue'].sum()` output. If they don't match, check for:
- double-counting from a many-to-many relationship
- a filter accidentally applied to a visual
- currency/rounding differences
