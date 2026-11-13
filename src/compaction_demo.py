
import pandas as pd
from pathlib import Path

SOURCE = Path("data/processed/orders")
FRAGMENTED = Path("data/fragmented/orders")
COMPACTED = Path("data/compacted/orders")

PARTITION_COLUMNS = ["year", "month", "day"]


def get_file_stats(folder):
    files = list(folder.rglob("*.parquet"))
    total_size = sum(file.stat().st_size for file in files)
    return len(files), total_size


def create_small_files():

    print("Creating fragmented dataset...")

    orders = pd.read_parquet(SOURCE)

    for keys, group in orders.groupby(PARTITION_COLUMNS):

        year, month, day = keys

        folder = (
            FRAGMENTED
            / f"year={year}"
            / f"month={month}"
            / f"day={day}"
        )

        folder.mkdir(parents=True, exist_ok=True)

        # Remove partition columns from the physical file
        group = group.drop(columns=PARTITION_COLUMNS)

        # Split each date into chunks of 250 records
        for i, start in enumerate(range(0, len(group), 250)):

            chunk = group.iloc[start:start + 250]

            chunk.to_parquet(
                folder / f"part-{i}.parquet",
                index=False
            )

    print("Fragmented dataset created!")


def compact_files():

    print("\nStarting compaction...")

    for folder in FRAGMENTED.rglob("day=*"):

        files = list(folder.glob("*.parquet"))

        if not files:
            continue

        # Read all small files in this date partition
        frames = [pd.read_parquet(file) for file in files]

        combined = pd.concat(frames, ignore_index=True)

        relative_folder = folder.relative_to(FRAGMENTED)
        output_folder = COMPACTED / relative_folder

        output_folder.mkdir(parents=True, exist_ok=True)

        # Write one combined file for this date
        combined.to_parquet(
            output_folder / "part-0.parquet",
            index=False
        )

    print("Compaction completed!")


def main():

    # Avoid mixing results from previous runs
    import shutil

    for folder in [FRAGMENTED, COMPACTED]:
        if folder.exists():
            shutil.rmtree(folder)

    create_small_files()

    before_count, before_size = get_file_stats(FRAGMENTED)

    compact_files()

    after_count, after_size = get_file_stats(COMPACTED)

    print("\n===== COMPACTION REPORT =====")
    print("Before compaction:")
    print("Files:", before_count)
    print("Size (KB):", round(before_size / 1024, 2))

    print("\nAfter compaction:")
    print("Files:", after_count)
    print("Size (KB):", round(after_size / 1024, 2))

    print("\nFiles reduced:", before_count - after_count)

    # Verify record counts
    original_rows = len(pd.read_parquet(SOURCE))
    compacted_rows = len(pd.read_parquet(COMPACTED))

    print("\nOriginal records:", original_rows)
    print("Compacted records:", compacted_rows)
    print("Record counts match:", original_rows == compacted_rows)


if __name__ == "__main__":
    main()
