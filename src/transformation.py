
import pandas as pd

def transform_data(orders):

    # Create a copy of the valid data
    orders = orders.copy()

    # Convert order_date into datetime format
    orders["order_date"] = pd.to_datetime(
        orders["order_date"]
    )

    # Convert ID columns into integer format
    orders["order_id"] = orders["order_id"].astype("int64")
    orders["customer_id"] = orders["customer_id"].astype("int64")

    # Convert amount into numeric format
    orders["amount"] = pd.to_numeric(orders["amount"])

    # Round amount to two decimal places
    orders["amount"] = orders["amount"].round(2)

    # Extract year, month, and day
    orders["year"] = orders["order_date"].dt.year
    orders["month"] = orders["order_date"].dt.month
    orders["day"] = orders["order_date"].dt.day

    print("Data transformation completed!")
    print("Total transformed records:", len(orders))
    print("New columns:", ["year", "month", "day"])

    return orders


