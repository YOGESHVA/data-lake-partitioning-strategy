
from ingestion import load_raw_data
from validation import validate_data
from transformation import transform_data
from partitioning import partition_data

def run_pipeline():

    print("===== DATA LAKE PIPELINE STARTED =====")

    # Step 1: Ingestion
    orders = load_raw_data()

    # Step 2: Validation
    valid, rejected = validate_data(orders)

    # Step 3: Transformation
    transformed = transform_data(valid)

    # Step 4: Partitioning
    output_folder = partition_data(transformed)

    print("\n===== PIPELINE SUMMARY =====")
    print("Input records:", len(orders))
    print("Valid records:", len(valid))
    print("Rejected records:", len(rejected))
    print("Transformed records:", len(transformed))
    print("Partitioned data:", output_folder)

    print("\nPipeline execution completed!")


if __name__ == "__main__":
    run_pipeline()
