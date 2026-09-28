"""
00_generate_dataset.py
Generates a realistic synthetic Indian kirana/supermarket dataset.

Outputs (in ../data/):
    customers.csv
    products.csv
    sales.csv
    inventory.csv
    suppliers.csv

Run:
    python 00_generate_dataset.py
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
import os

# ----------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------
SEED = 42
np.random.seed(SEED)
random.seed(SEED)

N_CUSTOMERS = 1200
N_PRODUCTS = 80
N_SUPPLIERS = 15
N_SALES_ROWS = 55000
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 12, 31)
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUT_DIR, exist_ok=True)

CITIES = ["Chennai", "Coimbatore", "Madurai", "Trichy", "Salem", "Vellore", "Erode", "Tirunelveli"]
STORE_LOCATIONS = ["Anna Nagar", "T Nagar", "Velachery", "Adyar", "Porur"]
SEGMENTS = ["Regular", "Premium", "Occasional", "New"]
PAYMENT_METHODS = ["Cash", "UPI", "Card", "Wallet"]

CATEGORIES = {
    "Grocery": ["Rice", "Wheat Flour", "Pulses", "Sugar", "Salt", "Cooking Oil"],
    "Dairy": ["Milk", "Curd", "Paneer", "Butter", "Cheese"],
    "Snacks": ["Biscuits", "Chips", "Namkeen", "Chocolates"],
    "Beverages": ["Tea", "Coffee", "Soft Drinks", "Juices"],
    "Personal Care": ["Soap", "Shampoo", "Toothpaste", "Hair Oil"],
    "Household": ["Detergent", "Dishwash", "Room Freshener", "Cleaning Liquid"],
    "Vegetables": ["Onion", "Potato", "Tomato", "Leafy Greens"],
    "Bakery": ["Bread", "Cake", "Buns", "Rusk"],
}

BRANDS = ["Aashirvaad", "Tata", "ITC", "HUL", "Amul", "Britannia", "Nestle", "Patanjali",
          "Local Brand", "Parle", "Dabur", "Godrej"]

# ----------------------------------------------------------------------
# 1. SUPPLIERS
# ----------------------------------------------------------------------
suppliers = pd.DataFrame({
    "supplier_id": [f"SUP{str(i).zfill(3)}" for i in range(1, N_SUPPLIERS + 1)],
    "supplier_name": [f"{random.choice(['Sri','Om','Sai','Kaveri','Amman','Balaji'])} "
                       f"{random.choice(['Traders','Distributors','Agencies','Enterprises','Wholesale'])}"
                       for _ in range(N_SUPPLIERS)],
    "supplier_location": [random.choice(CITIES) for _ in range(N_SUPPLIERS)],
    "lead_time_days": np.random.randint(2, 15, N_SUPPLIERS),
    "supplier_rating": np.round(np.random.uniform(2.5, 5.0, N_SUPPLIERS), 1),
})

# ----------------------------------------------------------------------
# 2. PRODUCTS
# ----------------------------------------------------------------------
product_rows = []
pid = 1
cat_list = list(CATEGORIES.items())
for i in range(N_PRODUCTS):
    category, subcats = cat_list[i % len(cat_list)]
    sub_category = random.choice(subcats)
    brand = random.choice(BRANDS)
    unit = random.choice(["kg", "litre", "packet", "piece", "gram"])

    # Realistic price bands by category
    base_cost = {
        "Grocery": (30, 120), "Dairy": (20, 90), "Snacks": (10, 60),
        "Beverages": (15, 150), "Personal Care": (25, 200),
        "Household": (20, 180), "Vegetables": (10, 50), "Bakery": (15, 80),
    }[category]
    cost_price = round(np.random.uniform(*base_cost), 2)

    # Margin varies: some categories intentionally high-margin, some low
    margin_pct = {
        "Grocery": 0.12, "Dairy": 0.15, "Snacks": 0.28, "Beverages": 0.25,
        "Personal Care": 0.35, "Household": 0.30, "Vegetables": 0.10, "Bakery": 0.20,
    }[category]
    margin_pct += np.random.uniform(-0.05, 0.08)  # noise so not every product identical
    selling_price = round(cost_price * (1 + max(margin_pct, 0.05)), 2)

    product_rows.append({
        "product_id": f"P{str(pid).zfill(4)}",
        "product_name": f"{brand} {sub_category}",
        "category": category,
        "sub_category": sub_category,
        "brand": brand,
        "unit": unit,
        "cost_price": cost_price,
        "selling_price": selling_price,
        "supplier_id": random.choice(suppliers["supplier_id"].tolist()),
    })
    pid += 1

products = pd.DataFrame(product_rows)

# Assign a "popularity weight" per product so sales aren't uniform random
# (some products are best-sellers, some are slow-moving) - stored only in-memory
popularity = np.random.pareto(a=1.8, size=len(products)) + 0.1
popularity = popularity / popularity.sum()
products["_popularity"] = popularity  # helper column, dropped before export

# ----------------------------------------------------------------------
# 3. CUSTOMERS
# ----------------------------------------------------------------------
FIRST_NAMES = ["Arjun", "Priya", "Karthik", "Divya", "Suresh", "Lakshmi", "Ravi", "Meena",
               "Vijay", "Anitha", "Senthil", "Kavya", "Muthu", "Deepa", "Ganesh", "Sowmya"]
LAST_NAMES = ["Kumar", "Raj", "Prakash", "Iyer", "Nair", "Pillai", "Reddy", "Krishnan", "Murthy"]

reg_dates = pd.to_datetime(
    np.random.choice(pd.date_range(START_DATE - timedelta(days=730), END_DATE), N_CUSTOMERS)
)

customers = pd.DataFrame({
    "customer_id": [f"C{str(i).zfill(5)}" for i in range(1, N_CUSTOMERS + 1)],
    "customer_name": [f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}" for _ in range(N_CUSTOMERS)],
    "gender": np.random.choice(["Male", "Female"], N_CUSTOMERS, p=[0.52, 0.48]),
    "age": np.random.randint(18, 70, N_CUSTOMERS),
    "city": np.random.choice(CITIES, N_CUSTOMERS, p=[0.30, 0.15, 0.12, 0.12, 0.10, 0.08, 0.08, 0.05]),
    "customer_segment": np.random.choice(SEGMENTS, N_CUSTOMERS, p=[0.45, 0.20, 0.25, 0.10]),
    "registration_date": reg_dates.strftime("%Y-%m-%d"),
})

# Customer purchase-frequency weight: "Regular"/"Premium" buy more often (repeat customers)
freq_weight = customers["customer_segment"].map({
    "Regular": 1.5, "Premium": 2.0, "Occasional": 0.6, "New": 0.4
}).values
freq_weight = freq_weight / freq_weight.sum()

# ----------------------------------------------------------------------
# 4. SALES (with weekly/seasonal patterns)
# ----------------------------------------------------------------------
date_range = pd.date_range(START_DATE, END_DATE)

# Weekly pattern: weekends higher; seasonal: festive bump in Oct-Nov, dip in June
def day_weight(d):
    w = 1.0
    if d.weekday() in (5, 6):        # Sat/Sun
        w *= 1.35
    if d.month in (10, 11):          # festive season
        w *= 1.5
    if d.month == 6:                 # slow month
        w *= 0.8
    if d.month == 12:                # year-end
        w *= 1.2
    return w

day_weights = np.array([day_weight(d) for d in date_range])
day_weights = day_weights / day_weights.sum()

sale_dates = np.random.choice(date_range, N_SALES_ROWS, p=day_weights)
sale_customers = np.random.choice(customers["customer_id"].values, N_SALES_ROWS, p=freq_weight)
sale_products = np.random.choice(products["product_id"].values, N_SALES_ROWS, p=products["_popularity"].values)

quantities = np.random.choice([1, 2, 3, 4, 5], N_SALES_ROWS, p=[0.45, 0.25, 0.15, 0.10, 0.05])
discounts = np.round(np.random.choice([0, 0, 0, 5, 10, 15], N_SALES_ROWS, p=[0.5, 0.15, 0.1, 0.1, 0.1, 0.05]), 2)
payment = np.random.choice(PAYMENT_METHODS, N_SALES_ROWS, p=[0.30, 0.45, 0.18, 0.07])
store_loc = np.random.choice(STORE_LOCATIONS, N_SALES_ROWS)

sales = pd.DataFrame({
    "sale_id": [f"S{str(i).zfill(6)}" for i in range(1, N_SALES_ROWS + 1)],
    "sale_date": pd.to_datetime(sale_dates).strftime("%Y-%m-%d"),
    "customer_id": sale_customers,
    "product_id": sale_products,
    "quantity": quantities,
    "discount": discounts,
    "payment_method": payment,
    "store_location": store_loc,
})

products = products.drop(columns=["_popularity"])

# ----------------------------------------------------------------------
# 5. INVENTORY (daily, per product) — mathematically consistent
# ----------------------------------------------------------------------
sales["quantity"] = sales["quantity"].astype(int)
daily_sold = (
    sales.groupby(["sale_date", "product_id"])["quantity"].sum().reset_index()
)
daily_sold["sale_date"] = pd.to_datetime(daily_sold["sale_date"])

inventory_rows = []
# starting stock per product — sized relative to each product's own demand
# so some products start comfortable and others start tight (drives realistic
# REORDER NOW / LOW STOCK / OVERSTOCK spread instead of everything overstocked)
avg_daily_demand = daily_sold.groupby("product_id")["quantity"].mean().to_dict()
current_stock = {
    pid: int(max(avg_daily_demand.get(pid, 3), 1) * np.random.uniform(3, 25))
    for pid in products["product_id"]
}

sold_lookup = daily_sold.set_index(["sale_date", "product_id"])["quantity"].to_dict()

# restock probability/size also scaled to demand, and a bit stingier so
# closing stock trends down toward realistic reorder territory over the year
for d in date_range:
    for pid in products["product_id"]:
        opening = current_stock[pid]
        sold = int(sold_lookup.get((d, pid), 0))
        received = 0
        if random.random() < 0.09:  # restock roughly every ~11 days
            received = int(np.random.uniform(0.5, 1.1) * max(avg_daily_demand.get(pid, 3), 3) * 7)
        damaged = np.random.binomial(1, 0.03) * random.randint(1, 3)  # rare damage events
        closing = max(opening + received - sold - damaged, 0)

        inventory_rows.append({
            "inventory_date": d.strftime("%Y-%m-%d"),
            "product_id": pid,
            "opening_stock": opening,
            "received_stock": received,
            "sold_quantity": sold,
            "closing_stock": closing,
            "damaged_quantity": damaged,
        })
        current_stock[pid] = closing

inventory = pd.DataFrame(inventory_rows)

# ----------------------------------------------------------------------
# 6. INTENTIONAL DATA QUALITY ISSUES (for the Excel cleaning stage)
# ----------------------------------------------------------------------
raw_sales = sales.copy()

# a) inject duplicate rows
dup_idx = np.random.choice(raw_sales.index, 150, replace=False)
raw_sales = pd.concat([raw_sales, raw_sales.loc[dup_idx]], ignore_index=True)

# b) inject missing payment_method
miss_idx = np.random.choice(raw_sales.index, 200, replace=False)
raw_sales.loc[miss_idx, "payment_method"] = np.nan

# c) inject inconsistent text casing / whitespace in store_location
messy_idx = np.random.choice(raw_sales.index, 300, replace=False)
raw_sales.loc[messy_idx, "store_location"] = raw_sales.loc[messy_idx, "store_location"].str.upper() + "  "

# d) inject a few negative/invalid quantities (data entry errors)
bad_idx = np.random.choice(raw_sales.index, 25, replace=False)
raw_sales.loc[bad_idx, "quantity"] = -1

# e) inject a few impossible discount values (>100)
bad_disc_idx = np.random.choice(raw_sales.index, 15, replace=False)
raw_sales.loc[bad_disc_idx, "discount"] = 150

raw_sales = raw_sales.sample(frac=1, random_state=SEED).reset_index(drop=True)

# ----------------------------------------------------------------------
# EXPORT
# ----------------------------------------------------------------------
customers.to_csv(os.path.join(OUT_DIR, "customers.csv"), index=False)
products.to_csv(os.path.join(OUT_DIR, "products.csv"), index=False)
sales.to_csv(os.path.join(OUT_DIR, "sales.csv"), index=False)              # clean version (for SQL/Python)
raw_sales.to_csv(os.path.join(OUT_DIR, "raw_sales.csv"), index=False)     # messy version (for Excel exercise)
inventory.to_csv(os.path.join(OUT_DIR, "inventory.csv"), index=False)
suppliers.to_csv(os.path.join(OUT_DIR, "suppliers.csv"), index=False)

print("Dataset generated successfully in:", OUT_DIR)
print(f"customers: {len(customers)} rows")
print(f"products:  {len(products)} rows")
print(f"sales (clean): {len(sales)} rows")
print(f"raw_sales (messy, for Excel): {len(raw_sales)} rows")
print(f"inventory: {len(inventory)} rows")
print(f"suppliers: {len(suppliers)} rows")
