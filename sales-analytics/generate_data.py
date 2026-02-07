"""
Synthetic Data Generator for Sales Analytics Platform.

Generates sample sales data based on the project requirements specification.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


def generate_sales_data(
    n_orders: int = 200, output_path: str | None = None, seed: int = 42
) -> pd.DataFrame:
    """
    Generate synthetic sales data for testing and development.

    Args:
        n_orders: Number of orders to generate
        output_path: Optional path to save the CSV file

    Returns:
        DataFrame containing generated sales data
    """
    np.random.seed(seed)

    categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books"]
    products = {
        "Electronics": ["Laptop", "Phone", "Tablet", "Headphones"],
        "Clothing": ["T-Shirt", "Jeans", "Jacket", "Shoes"],
        "Home & Garden": ["Lamp", "Plant", "Cushion", "Rug"],
        "Sports": ["Yoga Mat", "Dumbbell", "Running Shoes", "Bike"],
        "Books": ["Fiction", "Science", "History", "Art"],
    }

    orders = []
    start_date = datetime(2023, 1, 1)

    for i in range(n_orders):
        category = np.random.choice(categories)
        product = np.random.choice(products[category])
        qty = np.random.randint(1, 5)
        unit_price = round(np.random.uniform(10, 500), 2)
        amount = qty * unit_price
        status = np.random.choice(
            ["completed", "pending", "cancelled", np.nan], p=[0.7, 0.15, 0.1, 0.05]
        )

        orders.append(
            {
                "order_id": f"ORD{1000 + i}",
                "customer_id": f"CUST{np.random.randint(1, 50)}",
                "order_date": start_date + timedelta(days=np.random.randint(0, 365)),
                "product_category": category,
                "product_name": product,
                "quantity": qty,
                "unit_price": unit_price,
                "order_amount": round(amount, 2),
                "status": status,
            }
        )

    df = pd.DataFrame(orders)

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Generated {n_orders} orders and saved to {output_path}")

    return df


# skip
if __name__ == "__main__":
    # Generate data and save to the data directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "data", "sales_data.csv")
    generate_sales_data(200, output_path)
