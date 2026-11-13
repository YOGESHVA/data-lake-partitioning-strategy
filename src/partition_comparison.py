
import pandas as pd
from pathlib import Path
import shutil
import duckdb

SOURCE = Path("data/processed/orders")
MONTHLY = Path("data/processed/monthly_orders")


def create_monthly_partitions():

    print("Creating monthly partitions...")

    if MONTHLY.exists():
        shutil.rmtree(MONTHLY)

    orders = pd.read_parquet(SOURCE)

    orders.to_parquet(
        MONTHLY,
        engine="pyarrow",
        partition_cols=["year", "month"],
        index=False
    )

    print("Monthly partitioning completed!")


def compare_files():

    daily_files = list(SOURCE.rglob("*.parquet"))
    monthly_files = list(MONTHLY.rglob("*.parquet"))

    print("\n===== FILE COUNT COMPARISON =====")
    print("Daily partition files:", len(daily_files))
    print("Monthly partition files:", len(monthly_files))


def compare_queries():

    con = duckdb.connect()

    daily_query = """
    SELECT COUNT(*)
    FROM read_parquet(
        'data/processed/orders/**/*.parquet',
        hive_partitioning=true
    )
    WHERE year=2026 AND month=11 AND day=11
    """

    monthly_query = """
    SELECT COUNT(*)
    FROM read_parquet(
        'data/processed/monthly_orders/**/*.parquet',
        hive_partitioning=true
    )
    WHERE year=2026 AND month=11 AND day=11
    """

    daily_result = con.execute(daily_query).fetchone()[0]
    monthly_result = con.execute(monthly_query).fetchone()[0]

    print("\n===== DAILY QUERY COMPARISON =====")
    print("Daily partition result:", daily_result)
    print("Monthly partition result:", monthly_result)
    print("Results match:", daily_result == monthly_result)

    print("\n===== DAILY PARTITION PLAN =====")
    for row in con.execute(
        "EXPLAIN ANALYZE " + daily_query
    ).fetchall():
        print(row[1])

    print("\n===== MONTHLY PARTITION PLAN =====")
    for row in con.execute(
        "EXPLAIN ANALYZE " + monthly_query
    ).fetchall():
        print(row[1])

    con.close()


if __name__ == "__main__":

    create_monthly_partitions()
    compare_files()
    compare_queries()

