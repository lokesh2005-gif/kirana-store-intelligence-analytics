"""
02_data_cleaning.py
Cleans raw_sales.csv (removes duplicates, fixes text formatting,
handles missing values, removes invalid rows) and saves cleaned_sales.csv.

Run: python 02_data_cleaning.py
"""
import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def main():
    df = pd.read_csv(os.path.join(DATA_DIR, "raw_sales.csv"))
    before = len(df)

    # 1. Remove exact duplicate rows
    df = df.drop_duplicates()

    # 2. Standardize text columns: strip whitespace, title-case store_location
    df["store_location"] = df["store_location"].str.strip().str.title()

    # 3. Fill missing payment_method with 'Unknown' (explainable choice, not deletion)
    df["payment_method"] = df["payment_method"].fillna("Unknown")

    # 4. Remove invalid quantities (negative/zero — data entry errors)
    df = df[df["quantity"] > 0]

    # 5. Cap/remove invalid discounts (>100 is impossible)
    df = df[(df["discount"] >= 0) & (df["discount"] <= 100)]

    # 6. Ensure sale_date is a valid date
    df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")
    df = df.dropna(subset=["sale_date"])

    after = len(df)
    print(f"Rows before cleaning: {before}")
    print(f"Rows after cleaning:  {after}")
    print(f"Rows removed:         {before - after}")

    df.to_csv(os.path.join(DATA_DIR, "cleaned_sales.csv"), index=False)
    print("Saved cleaned_sales.csv")

if __name__ == "__main__":
    main()
