"""
Data Generator for Sales Analytics Platform
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_sample_data(n_orders=200):
    """Generate synthetic sales data for analysis"""
    np.random.seed(42)

    categories = ["Electronics", "Clothing",
                  "Home & Garden", "Sports", "Books"]

    products = {
        "Electronics": ["Laptop", "Phone", "Tablet", "Headphones"],
        "Clothing": ["T-Shirt", "Jeans", "Jacket", "Shoes"],
        "Home & Garden": ["Lamp", "Plant", "Cushion", "Rug"],
        "Sports": ["Yoga Mat", "Dumbbell", "Running Shoes", "Bike"],
        "Books": ["Fiction", "Science", "History", "Art"]
    }

    orders = []
    start_date = datetime(2023, 1, 1)

    for i in range(n_orders):
        category = np.random.choice(categories)
        product = np.random.choice(products[category])
        qty = np.random.randint(1, 5)
        unit_price = np.random.uniform(10, 500)
        amount = qty * unit_price
        status = np.random.choice(
            ["completed", "pending", "cancelled", np.nan],
            p=[0.7, 0.15, 0.1, 0.05]
        )

        orders.append({
            "order_id": f"ORD{1000+i}",
            "customer_id": f"CUST{np.random.randint(1, 50)}",
            "order_date": (start_date + timedelta(days=np.random.randint(0, 365))).strftime("%Y-%m-%d"),
            "product_category": category,
            "product_name": product,
            "quantity": qty,
            "unit_price": round(unit_price, 2),
            "order_amount": round(amount, 2),
            "status": status
        })

    df = pd.DataFrame(orders)
    df.to_csv("data/sales_data.csv", index=False)
    print(f"✅ Generated {n_orders} orders in data/sales_data.csv")
    print(f"📊 Data shape: {df.shape}")
    print(
        f"📅 Date range: {df['order_date'].min()} to {df['order_date'].max()}")

    return df


if __name__ == "__main__":
    print("=== SALES DATA GENERATOR ===")
    df = generate_sample_data()
    print("\n📋 Sample Data (first 5 rows):")
    print(df.head())
    print("\n✅ Data generation complete!")
