"""
01_data_validation.py
Validates schemas, checks missing values, duplicates, and invalid IDs
on the RAW (messy) sales data plus the other tables.

Run: python 01_data_validation.py
"""
import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def load():
    customers = pd.read_csv(os.path.join(DATA_DIR, "customers.csv"))
    products = pd.read_csv(os.path.join(DATA_DIR, "products.csv"))
    raw_sales = pd.read_csv(os.path.join(DATA_DIR, "raw_sales.csv"))
    inventory = pd.read_csv(os.path.join(DATA_DIR, "inventory.csv"))
    suppliers = pd.read_csv(os.path.join(DATA_DIR, "suppliers.csv"))
    return customers, products, raw_sales, inventory, suppliers

def report(name, df):
    print(f"\n--- {name} ---")
    print("Shape:", df.shape)
    print("Missing values:\n", df.isna().sum()[df.isna().sum() > 0])
    print("Duplicate rows:", df.duplicated().sum())

def main():
    customers, products, raw_sales, inventory, suppliers = load()

    for name, df in [("customers", customers), ("products", products),
                      ("raw_sales", raw_sales), ("inventory", inventory),
                      ("suppliers", suppliers)]:
        report(name, df)

    # Invalid ID checks
    bad_customers = raw_sales[~raw_sales["customer_id"].isin(customers["customer_id"])]
    bad_products = raw_sales[~raw_sales["product_id"].isin(products["product_id"])]
    print(f"\nInvalid customer_id references in raw_sales: {len(bad_customers)}")
    print(f"Invalid product_id references in raw_sales: {len(bad_products)}")

    # Invalid business values
    print(f"Negative/zero quantities: {(raw_sales['quantity'] <= 0).sum()}")
    print(f"Invalid discounts (>100 or <0): {((raw_sales['discount']>100)|(raw_sales['discount']<0)).sum()}")

if __name__ == "__main__":
    main()
