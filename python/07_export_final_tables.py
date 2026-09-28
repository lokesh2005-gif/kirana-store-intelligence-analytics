"""
07_export_final_tables.py
Exports the final star-schema-ready fact/dim tables for Power BI.

Outputs (in ../data/final/):
    FactSales.csv
    FactInventory.csv
    DimProduct.csv
    DimCustomer.csv
    DimSupplier.csv
    DimDate.csv
    reorder_recommendations.csv (copied)

Run: python 07_export_final_tables.py
"""
import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
FINAL_DIR = os.path.join(DATA_DIR, "final")
os.makedirs(FINAL_DIR, exist_ok=True)

def main():
    sales = pd.read_csv(os.path.join(DATA_DIR, "sales_enriched.csv"), parse_dates=["sale_date"])
    products = pd.read_csv(os.path.join(DATA_DIR, "products.csv"))
    customers = pd.read_csv(os.path.join(DATA_DIR, "customers.csv"))
    suppliers = pd.read_csv(os.path.join(DATA_DIR, "suppliers.csv"))
    inventory = pd.read_csv(os.path.join(DATA_DIR, "inventory.csv"), parse_dates=["inventory_date"])
    reorder = pd.read_csv(os.path.join(DATA_DIR, "reorder_recommendations.csv"))

    # FactSales: keep only keys + measures (no descriptive attributes -> avoid duplication with dims)
    fact_sales = sales[[
        "sale_id", "sale_date", "customer_id", "product_id",
        "quantity", "discount", "payment_method", "store_location",
        "revenue", "cost", "profit", "profit_margin_pct"
    ]]
    fact_sales.to_csv(os.path.join(FINAL_DIR, "FactSales.csv"), index=False)

    # FactInventory
    inventory.to_csv(os.path.join(FINAL_DIR, "FactInventory.csv"), index=False)

    # DimProduct
    products.to_csv(os.path.join(FINAL_DIR, "DimProduct.csv"), index=False)

    # DimCustomer
    customers.to_csv(os.path.join(FINAL_DIR, "DimCustomer.csv"), index=False)

    # DimSupplier
    suppliers.to_csv(os.path.join(FINAL_DIR, "DimSupplier.csv"), index=False)

    # DimDate
    min_date = min(sales["sale_date"].min(), inventory["inventory_date"].min())
    max_date = max(sales["sale_date"].max(), inventory["inventory_date"].max())
    dim_date = pd.DataFrame({"date": pd.date_range(min_date, max_date)})
    dim_date["year"] = dim_date["date"].dt.year
    dim_date["month"] = dim_date["date"].dt.month
    dim_date["month_name"] = dim_date["date"].dt.month_name()
    dim_date["day"] = dim_date["date"].dt.day
    dim_date["day_name"] = dim_date["date"].dt.day_name()
    dim_date["week_of_year"] = dim_date["date"].dt.isocalendar().week
    dim_date["quarter"] = dim_date["date"].dt.quarter
    dim_date["year_month"] = dim_date["date"].dt.to_period("M").astype(str)
    dim_date.to_csv(os.path.join(FINAL_DIR, "DimDate.csv"), index=False)

    # Reorder recommendations (already final)
    reorder.to_csv(os.path.join(FINAL_DIR, "reorder_recommendations.csv"), index=False)

    print("Final tables exported to:", FINAL_DIR)
    for f in os.listdir(FINAL_DIR):
        path = os.path.join(FINAL_DIR, f)
        print(f" - {f}: {sum(1 for _ in open(path)) - 1} rows")

if __name__ == "__main__":
    main()
