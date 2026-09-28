"""
06_reorder_recommendation.py
Builds the explainable Smart Reorder System.

Formulas:
    Reorder Point = (Average Daily Demand x Lead Time) + Safety Stock
    Safety Stock  = Average Daily Demand x Safety Buffer Days (default 3 days)
    Recommended Order Qty = max(Reorder Point - Current Stock, 0) rounded up,
                             but topped up to cover Forecast Demand over lead time
                             if forecast demand is higher than the historical average.

Stock status:
    REORDER NOW  -> current_stock == 0
    LOW STOCK    -> 0 < current_stock <= reorder_point
    OVERSTOCK    -> current_stock > reorder_point * 3
    HEALTHY      -> everything else

Run: python 06_reorder_recommendation.py
"""
import pandas as pd
import os
import math

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
SAFETY_BUFFER_DAYS = 3

def main():
    products = pd.read_csv(os.path.join(DATA_DIR, "products.csv"))
    suppliers = pd.read_csv(os.path.join(DATA_DIR, "suppliers.csv"))
    demand = pd.read_csv(os.path.join(DATA_DIR, "demand_summary.csv"))
    inventory = pd.read_csv(os.path.join(DATA_DIR, "inventory.csv"), parse_dates=["inventory_date"])

    # Latest closing stock per product = "current stock"
    latest_date = inventory["inventory_date"].max()
    current_stock = (
        inventory[inventory["inventory_date"] == latest_date][["product_id", "closing_stock"]]
        .rename(columns={"closing_stock": "current_stock"})
    )

    df = products.merge(suppliers, on="supplier_id", how="left")
    df = df.merge(demand, on="product_id", how="left")
    df = df.merge(current_stock, on="product_id", how="left")

    df["average_daily_demand"] = df["average_daily_demand"].fillna(0)
    df["forecast_demand_per_day"] = df["forecast_demand_per_day"].fillna(0)
    df["current_stock"] = df["current_stock"].fillna(0)

    df["safety_stock"] = (df["average_daily_demand"] * SAFETY_BUFFER_DAYS).apply(math.ceil)
    df["reorder_point"] = (
        (df["average_daily_demand"] * df["lead_time_days"]) + df["safety_stock"]
    ).apply(math.ceil)

    # Forecast demand over the lead time (uses the more responsive moving-avg forecast)
    df["forecast_demand"] = (df["forecast_demand_per_day"] * df["lead_time_days"]).round().astype(int)

    def order_qty(row):
        base_need = max(row["reorder_point"] - row["current_stock"], 0)
        forecast_need = max(row["forecast_demand"] + row["safety_stock"] - row["current_stock"], 0)
        return int(math.ceil(max(base_need, forecast_need)))

    df["recommended_order_qty"] = df.apply(order_qty, axis=1)

    def status(row):
        if row["current_stock"] == 0:
            return "REORDER NOW"
        elif row["current_stock"] <= row["reorder_point"]:
            return "LOW STOCK"
        elif row["current_stock"] > row["reorder_point"] * 3:
            return "OVERSTOCK"
        else:
            return "HEALTHY"

    df["stock_status"] = df.apply(status, axis=1)

    final_cols = [
        "product_id", "product_name", "current_stock", "average_daily_demand",
        "forecast_demand", "lead_time_days", "safety_stock", "reorder_point",
        "recommended_order_qty", "stock_status"
    ]
    final = df[final_cols].sort_values("stock_status")

    out_path = os.path.join(DATA_DIR, "reorder_recommendations.csv")
    final.to_csv(out_path, index=False)

    print(f"Saved {out_path}")
    print(final["stock_status"].value_counts())
    print(final.head(10))

if __name__ == "__main__":
    main()
