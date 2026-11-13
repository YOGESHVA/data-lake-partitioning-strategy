
import pandas as pd
from pathlib import Path

def load_raw_data():
    # Locate the raw CSV file
    input_file = Path("data/raw/orders.csv")

    # Check whether the file exists
    if not input_file.exists():
        raise FileNotFoundError("Raw orders file not found!")

    # Read CSV into a Pandas DataFrame
    orders = pd.read_csv(input_file)

    # Display ingestion results
    print("Data ingestion completed successfully!")
    print("Total records loaded:", len(orders))
    print("Total columns:", len(orders.columns))
    print("Column names:", list(orders.columns))

    return orders


if __name__ == "__main__":
    orders = load_raw_data()
