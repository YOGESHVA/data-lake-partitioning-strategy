
import duckdb

# Connect to DuckDB
con = duckdb.connect()

# Read all date-partitioned Parquet files
source = """
read_parquet(
    'data/processed/orders/**/*.parquet',
    hive_partitioning = true
)
"""

# Query 1: Read all records
full_query = f"""
SELECT COUNT(*)
FROM {source}
"""

# Query 2: Read only November 11, 2026
filtered_query = f"""
SELECT COUNT(*)
FROM {source}
WHERE year = 2026
  AND month = 11
  AND day = 11
"""

full_count = con.execute(full_query).fetchone()[0]
filtered_count = con.execute(filtered_query).fetchone()[0]

print("===== PARTITION PRUNING DEMO =====")
print("Total records:", full_count)
print("Records on November 11:", filtered_count)

print("\n===== QUERY EXECUTION PLAN =====")

plan = con.execute(
    "EXPLAIN ANALYZE " + filtered_query
).fetchall()

for row in plan:
    print(row[1])

con.close()

