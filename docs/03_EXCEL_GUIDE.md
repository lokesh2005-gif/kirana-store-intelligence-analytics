# Part 3 — Excel Work Guide

Excel is the **data preparation and validation stage**, not the analysis engine.
Use `data/raw_sales.csv` (the intentionally messy file) for this exercise.

## Workbook structure: `Kirana_Analytics.xlsx`

| Sheet | Contents |
|---|---|
| `Raw_Sales` | Paste `raw_sales.csv` as-is (55,150 rows, with issues) |
| `Cleaned_Sales` | Your cleaned copy (or link to `cleaned_sales.csv` output) |
| `Products` | `products.csv` |
| `Customers` | `customers.csv` |
| `Inventory` | `inventory.csv` |
| `Data_Quality` | Your findings log (see below) |
| `Pivot_Analysis` | Pivot tables built from `Cleaned_Sales` |

## What to clean and how

1. **Duplicate rows** (raw file has 150 injected duplicates)
   `Data` tab → *Remove Duplicates*, or flag with:
   `=COUNTIFS($A$2:$A$55151,A2)>1`

2. **Missing `payment_method`** (200 blanks)
   Find with `=COUNTBLANK(F:F)`. Fill with "Unknown" using Find & Replace on blanks, or a formula:
   `=IF(F2="","Unknown",F2)`

3. **Inconsistent text casing/whitespace in `store_location`**
   `=TRIM(PROPER(G2))` to standardize, then paste values.

4. **Invalid quantities** (25 rows have `quantity = -1`)
   Flag with conditional formatting: `=D2<=0`, then filter and delete/investigate.

5. **Invalid discounts** (15 rows with `discount = 150`, impossible)
   Flag with `=E2>100`. Cap or remove.

## Data_Quality sheet — log these findings

| Check | Formula | Result |
|---|---|---|
| Duplicate rows | `=SUMPRODUCT((COUNTIFS(...)>1)*1)` | ~150 |
| Missing payment_method | `=COUNTBLANK(F:F)` | ~200 |
| Invalid quantity | `=COUNTIF(D:D,"<=0")` | ~25 |
| Invalid discount | `=COUNTIF(E:E,">100")` | ~15 |

## Basic calculations (add as helper columns in Cleaned_Sales)

- Revenue: `=Quantity*VLOOKUP(ProductID,Products!A:H,8,FALSE)*(1-Discount/100)`
- Cost: `=Quantity*VLOOKUP(ProductID,Products!A:H,7,FALSE)`
- Profit: `=Revenue-Cost`

## Pivot Tables to create (on `Pivot_Analysis` sheet)

1. **Revenue by Month** — Rows: Sale Date (grouped by Month), Values: Sum of Revenue
2. **Revenue by Category** — Rows: Category (via lookup column), Values: Sum of Revenue
3. **Top Products** — Rows: Product Name, Values: Sum of Quantity, sorted descending
4. **Payment Method Split** — Rows: Payment Method, Values: Count of Sale ID
5. **Store Location Performance** — Rows: Store Location, Values: Sum of Revenue

## Evidence to keep (for GitHub/resume proof)

- Screenshot of Data_Quality sheet with counts
- Screenshot of at least 2 Pivot Tables
- Screenshot of a conditional-formatting rule catching bad data

**Remember:** Excel proves you can inspect and clean data manually. The heavy
computation (profit, margin, demand, forecasting) is intentionally done in
Python/SQL — don't duplicate that work here.
