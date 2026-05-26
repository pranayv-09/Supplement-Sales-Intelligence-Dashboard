import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Reproducible random data
np.random.seed(42)

# -----------------------------
# Master Data
# -----------------------------

products = {
    "Hair Oil": 499,
    "Hair Serum": 699,
    "Hair Capsules": 899,
    "Detox Tea": 599,
    "Weight Control Capsules": 1199,
    "Skin Glow Tablets": 799,
    "Immunity Booster": 649
}

states = [
    "Delhi",
    "Maharashtra",
    "Karnataka",
    "Uttar Pradesh",
    "Bihar",
    "West Bengal",
    "Gujarat",
    "Rajasthan",
    "Punjab",
    "Haryana"
]

channels = [
    "Website",
    "Amazon",
    "Flipkart"
]

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "COD"
]

categories = {
    "Hair Oil": "Hair Care",
    "Hair Serum": "Hair Care",
    "Hair Capsules": "Hair Care",
    "Detox Tea": "Detox",
    "Weight Control Capsules": "Weight Management",
    "Skin Glow Tablets": "Beauty",
    "Immunity Booster": "Immunity"
}

# -----------------------------
# Generate Records
# -----------------------------

n_records = 10000

start_date = datetime(2024, 1, 1)

data = []

for i in range(n_records):

    product = np.random.choice(list(products.keys()))

    quantity = np.random.randint(1, 6)

    unit_price = products[product]

    revenue = quantity * unit_price

    order_date = start_date + timedelta(
        days=np.random.randint(0, 730)
    )

    record = {
        "Order_ID": f"ORD{i+1:05d}",
        "Order_Date": order_date,
        "Customer_ID": f"CUST{np.random.randint(1000,9999)}",
        "Age": np.random.randint(18, 60),
        "Gender": np.random.choice(
            ["Male", "Female"]
        ),
        "State": np.random.choice(states),
        "Product_Name": product,
        "Category": categories[product],
        "Quantity": quantity,
        "Unit_Price": unit_price,
        "Revenue": revenue,
        "Payment_Method": np.random.choice(payment_methods),
        "Channel": np.random.choice(channels),
        "Customer_Type": np.random.choice(
            ["New", "Repeat"],
            p=[0.4, 0.6]
        )
    }

    data.append(record)

# -----------------------------
# Create DataFrame
# -----------------------------

df = pd.DataFrame(data)

# -----------------------------
# Save CSV
# -----------------------------

output_path = "data/raw/supplement_sales.csv"

df.to_csv(output_path, index=False)

print("Dataset Generated Successfully")
print(f"Rows: {len(df)}")
print(f"Saved To: {output_path}")