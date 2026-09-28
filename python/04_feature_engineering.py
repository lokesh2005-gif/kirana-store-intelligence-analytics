"""
04_feature_engineering.py
Merges tables and creates Revenue, Cost, Profit, Profit Margin columns.
Saves sales_enriched.csv — the base table used by all later scripts.

Run: python 04_feature_engineering.py
"""
import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def main():
    sales = pd.read_csv(os.path.join(DATA_DIR, "cleaned_sales.csv"), parse_dates=["sale_date"])
    products = pd.read_csv(os.path.join(DATA_DIR, "products.csv"))
    customers = pd.read_csv(os.path.join(DATA_DIR, "customers.csv"))

    df = sales.merge(products, on="product_id", how="left")
    df = df.merge(customers, on="customer_id", how="left")

    df["revenue"] = df["quantity"] * df["selling_price"] * (1 - df["discount"] / 100)
    df["cost"] = df["quantity"] * df["cost_price"]
    df["profit"] = df["revenue"] - df["cost"]
    df["profit_margin_pct"] = (df["profit"] / df["revenue"] * 100).round(2)

    df["year"] = df["sale_date"].dt.year
    df["month"] = df["sale_date"].dt.month
    df["year_month"] = df["sale_date"].dt.to_period("M").astype(str)
    df["day_of_week"] = df["sale_date"].dt.day_name()

    out_path = os.path.join(DATA_DIR, "sales_enriched.csv")
    df.to_csv(out_path, index=False)

    print(f"Saved {out_path}")
    print(f"Rows: {len(df)}")
    print(f"Total revenue: {df['revenue'].sum():,.2f}")
    print(f"Total profit:  {df['profit'].sum():,.2f}")

if __name__ == "__main__":
    main()
