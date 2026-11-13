from pathlib import Path

def inspect_files():

    folder = Path("data/processed/orders")

    # Find all Parquet files inside the date partitions
    parquet_files = list(folder.rglob("*.parquet"))

    # Get the size of each file in bytes
    file_sizes = [
        file.stat().st_size
        for file in parquet_files
    ]

    total_size = sum(file_sizes)

    print("===== PARQUET FILE REPORT =====")
    print("Total Parquet files:", len(parquet_files))
    print("Total size (KB):", round(total_size / 1024, 2))

    if file_sizes:
        print("Smallest file (KB):", round(min(file_sizes) / 1024, 2))
        print("Largest file (KB):", round(max(file_sizes) / 1024, 2))
        print("Average file size (KB):", round(total_size / len(file_sizes) / 1024, 2))

    print("\nIndividual file sizes:")

    for file in parquet_files:
        print(file, "->", round(file.stat().st_size / 1024, 2), "KB")


if __name__ == "__main__":
    inspect_files()

