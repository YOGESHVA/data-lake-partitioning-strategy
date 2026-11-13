
import pandas as pd
import numpy as np
from pathlib import Path

# 1. Set a fixed random seed
np.random.seed(42)

# 2. Define the number of records
NUMBER_OF_RECORDS = 100_000

# 3. Generate unique order IDs
order_ids = np.arange(100001, 100001 + NUMBER_OF_RECORDS)

# 4. Generate customer IDs
customer_ids = np.random.randint(1000, 5000, NUMBER_OF_RECORDS)

# 5. Generate random order dates across 30 days
order_dates = pd.to_datetime(
    np.random.choice(
        pd.date_range("2026-10-15", "2026-11-13"),
        size=NUMBER_OF_RECORDS
    )
)

# 6. Generate order amounts
amounts = np.round(
    np.random.uniform(100, 10000, NUMBER_OF_RECORDS), 2
)

# 7. Generate order statuses
statuses = np.random.choice(
    ["Completed", "Pending", "Cancelled"],
    size=NUMBER_OF_RECORDS,
    p=[0.70, 0.20, 0.10]
)

# 8. Create a DataFrame
orders = pd.DataFrame({
    "order_id": order_ids,
    "customer_id": customer_ids,
    "order_date": order_dates,
    "amount": amounts,
    "status": statuses
})

# 9. Create the raw data folder
output_folder = Path("data/raw")
output_folder.mkdir(parents=True, exist_ok=True)

# 10. Save records as CSV
output_file = output_folder / "orders.csv"
orders.to_csv(output_file, index=False)

# 11. Display information
print("Dataset generated successfully!")
print("Total records:", len(orders))
print("Total columns:", len(orders.columns))
print("Date range:", orders["order_date"].min(), "to", orders["order_date"].max())
print("Output file:", output_file)
print("\nFirst 5 records:")
print(orders.head())


