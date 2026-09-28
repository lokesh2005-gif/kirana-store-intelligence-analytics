"""
05_demand_analysis.py
Calculates average daily demand per product and a simple, explainable
demand forecast using a moving average.

Why moving average for an MVP?
- Easy to explain to a non-technical store owner.
- No risk of overfitting on ~1 year of data with weekly/seasonal noise.
- Fast to compute, no model training/tuning needed.
- Good enough accuracy for reorder-point decisions, which is the actual
  business need here (not a research-grade forecast).

Run: python 05_demand_analysis.py
"""
import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
MOVING_AVG_WINDOW = 14  # days

def main():
    df = pd.read_csv(os.path.join(DATA_DIR, "sales_enriched.csv"), parse_dates=["sale_date"])

    daily_demand = (
        df.groupby(["product_id", "sale_date"])["quantity"].sum().reset_index()
    )

    # Build a full daily calendar per product (fill days with 0 sales)
    all_products = daily_demand["product_id"].unique()
    date_range = pd.date_range(daily_demand["sale_date"].min(), daily_demand["sale_date"].max())

    full_index = pd.MultiIndex.from_product([all_products, date_range], names=["product_id", "sale_date"])
    daily_demand_full = (
        daily_demand.set_index(["product_id", "sale_date"])
        .reindex(full_index, fill_value=0)
        .reset_index()
    )

    # Moving average forecast: average of last N days = forecast for next day
    daily_demand_full = daily_demand_full.sort_values(["product_id", "sale_date"])
    daily_demand_full["moving_avg_demand"] = (
        daily_demand_full.groupby("product_id")["quantity"]
        .transform(lambda x: x.rolling(MOVING_AVG_WINDOW, min_periods=1).mean())
    )

    # Average daily demand (overall) and latest forecast (last available moving avg)
    avg_daily_demand = daily_demand_full.groupby("product_id")["quantity"].mean().rename("average_daily_demand")
    latest_forecast = (
        daily_demand_full.sort_values("sale_date")
        .groupby("product_id")["moving_avg_demand"]
        .last()
        .rename("forecast_demand_per_day")
    )

    demand_summary = pd.concat([avg_daily_demand, latest_forecast], axis=1).reset_index()
    demand_summary["average_daily_demand"] = demand_summary["average_daily_demand"].round(2)
    demand_summary["forecast_demand_per_day"] = demand_summary["forecast_demand_per_day"].round(2)

    out_path = os.path.join(DATA_DIR, "demand_summary.csv")
    demand_summary.to_csv(out_path, index=False)
    print(f"Saved {out_path}")
    print(demand_summary.head())

if __name__ == "__main__":
    main()
