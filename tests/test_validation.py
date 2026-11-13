
import pandas as pd
from src.validation import validate_data


def create_sample_data():

    return pd.DataFrame({
        "order_id": [101, 102, 103, 104, 105],
        "customer_id": [201, 202, 203, 204, 205],
        "order_date": [
            "2026-11-10",
            "2026-11-11",
            "2026-11-12",
            "2026-11-12",
            "2026-11-13"
        ],
        "amount": [500, 600, -100, 800, 900],
        "status": [
            "Completed",
            "Pending",
            "Completed",
            "Unknown",
            "Completed"
        ]
    })


def test_valid_records():

    data = create_sample_data()

    valid, rejected = validate_data(data)

    assert len(valid) == 3
    assert len(rejected) == 2


def test_duplicate_order_ids():

    data = pd.DataFrame({
        "order_id": [101, 101],
        "customer_id": [201, 202],
        "order_date": ["2026-11-10", "2026-11-11"],
        "amount": [500, 600],
        "status": ["Completed", "Pending"]
    })

    valid, rejected = validate_data(data)

    assert len(valid) == 1
    assert len(rejected) == 1


def test_missing_values():

    data = create_sample_data()
    data.loc[0, "customer_id"] = None

    valid, rejected = validate_data(data)

    assert len(rejected) == 3

def test_negative_amount_rejected():

    data = create_sample_data()
    data.loc[0, "amount"] = -500

    valid, rejected = validate_data(data)

    assert len(rejected) == 3
    assert 101 in rejected["order_id"].values


def test_invalid_status_rejected():

    data = create_sample_data()
    data.loc[0, "status"] = "Unknown"

    valid, rejected = validate_data(data)

    assert len(rejected) == 3
    assert 101 in rejected["order_id"].values
