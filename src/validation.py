
import pandas as pd

def validate_data(orders):

    # Create a copy of the input data
    orders = orders.copy()

    # Check missing values
    missing_check = orders[
        orders.isnull().any(axis=1)
    ]

    # Check duplicate order IDs
    duplicate_check = orders[
        orders.duplicated(subset=["order_id"], keep="first")
    ]

    # Check invalid amounts
    amount_check = orders[
        orders["amount"] <= 0
    ]

    # Check invalid statuses
    valid_statuses = ["Completed", "Pending", "Cancelled"]

    status_check = orders[
        ~orders["status"].isin(valid_statuses)
    ]

    # Combine all invalid record indexes
    invalid_indices = (
        set(missing_check.index)
        | set(duplicate_check.index)
        | set(amount_check.index)
        | set(status_check.index)
    )

    # Separate rejected and valid records
    rejected = orders.loc[sorted(invalid_indices)].copy()
    valid = orders.drop(index=invalid_indices).copy()

    # Display validation results
    print("Data validation completed!")
    print("Total input records:", len(orders))
    print("Valid records:", len(valid))
    print("Rejected records:", len(rejected))

    return valid, rejected
