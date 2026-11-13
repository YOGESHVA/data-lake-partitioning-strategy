
from pathlib import Path
import shutil


def partition_data(orders):

    # Define output, temporary, and backup folders
    output_folder = Path("data/processed/orders")
    staging_folder = Path("data/processed/orders_staging")
    backup_folder = Path("data/processed/orders_backup")

    # Recover the previous output if an earlier replacement was interrupted
    if backup_folder.exists():

        if not output_folder.exists():
            backup_folder.rename(output_folder)
        else:
            shutil.rmtree(backup_folder)

    # Remove leftover temporary data from an earlier failed run
    if staging_folder.exists():
        shutil.rmtree(staging_folder)

    # Create the temporary folder
    staging_folder.mkdir(parents=True, exist_ok=True)

    try:

        # Write the new dataset into the temporary folder
        orders.to_parquet(
            staging_folder,
            engine="pyarrow",
            partition_cols=["year", "month", "day"],
            index=False
        )

        print("New partitioned data created in staging folder!")

        # Move the old output to backup
        if output_folder.exists():
            output_folder.rename(backup_folder)

        try:

            # Promote the new output
            staging_folder.rename(output_folder)

        except Exception:

            # Restore the previous output if promotion fails
            if backup_folder.exists() and not output_folder.exists():
                backup_folder.rename(output_folder)

            raise

        # Delete backup only after successful replacement
        if backup_folder.exists():
            shutil.rmtree(backup_folder)

        print("Date-based partitioning completed!")
        print("Partition columns: year, month, day")
        print("Output location:", output_folder)

        return output_folder

    except Exception:

        # Remove incomplete staging output
        if staging_folder.exists():
            shutil.rmtree(staging_folder)

        raise
