"""
03_eda.py
Exploratory Data Analysis: sales trends, product performance, customer behavior.
Saves charts as PNG files into ../docs/charts/

Run: python 03_eda.py
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CHART_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "charts")
os.makedirs(CHART_DIR, exist_ok=True)

sns.set_theme(style="whitegrid")

def main():
    sales = pd.read_csv(os.path.join(DATA_DIR, "cleaned_sales.csv"), parse_dates=["sale_date"])
    products = pd.read_csv(os.path.join(DATA_DIR, "products.csv"))
    customers = pd.read_csv(os.path.join(DATA_DIR, "customers.csv"))

    merged = sales.merge(products, on="product_id").merge(customers, on="customer_id")
    merged["revenue"] = merged["quantity"] * merged["selling_price"] * (1 - merged["discount"] / 100)
    merged["cost"] = merged["quantity"] * merged["cost_price"]
    merged["profit"] = merged["revenue"] - merged["cost"]

    # 1. Monthly revenue trend
    monthly = merged.set_index("sale_date").resample("ME")["revenue"].sum()
    plt.figure(figsize=(10, 5))
    monthly.plot(marker="o")
    plt.title("Monthly Revenue Trend")
    plt.ylabel("Revenue (INR)")
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_DIR, "monthly_revenue_trend.png"))
    plt.close()

    # 2. Category-wise revenue
    cat_rev = merged.groupby("category")["revenue"].sum().sort_values(ascending=False)
    plt.figure(figsize=(9, 5))
    sns.barplot(x=cat_rev.values, y=cat_rev.index, hue=cat_rev.index, palette="viridis", legend=False)
    plt.title("Revenue by Category")
    plt.xlabel("Revenue (INR)")
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_DIR, "category_revenue.png"))
    plt.close()

    # 3. Top 10 products
    top_products = merged.groupby("product_name")["revenue"].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(9, 5))
    sns.barplot(x=top_products.values, y=top_products.index, hue=top_products.index, palette="mako", legend=False)
    plt.title("Top 10 Products by Revenue")
    plt.xlabel("Revenue (INR)")
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_DIR, "top10_products.png"))
    plt.close()

    # 4. Customer segment distribution
    seg_rev = merged.groupby("customer_segment")["revenue"].sum().sort_values(ascending=False)
    plt.figure(figsize=(7, 5))
    sns.barplot(x=seg_rev.index, y=seg_rev.values, hue=seg_rev.index, palette="crest", legend=False)
    plt.title("Revenue by Customer Segment")
    plt.ylabel("Revenue (INR)")
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_DIR, "customer_segment_revenue.png"))
    plt.close()

    # 5. Day-of-week pattern
    merged["day_of_week"] = merged["sale_date"].dt.day_name()
    dow_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    dow_rev = merged.groupby("day_of_week")["revenue"].sum().reindex(dow_order)
    plt.figure(figsize=(9, 5))
    sns.barplot(x=dow_rev.index, y=dow_rev.values, hue=dow_rev.index, palette="flare", legend=False)
    plt.title("Revenue by Day of Week")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_DIR, "day_of_week_revenue.png"))
    plt.close()

    print("EDA complete. Charts saved to:", CHART_DIR)
    print("\nSummary stats:")
    print(f"Total revenue: {merged['revenue'].sum():,.2f}")
    print(f"Total profit:  {merged['profit'].sum():,.2f}")
    print(f"Total orders:  {merged['sale_id'].nunique():,}")
    print(f"Total customers who purchased: {merged['customer_id'].nunique():,}")

if __name__ == "__main__":
    main()
