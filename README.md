\# Data Lake Partitioning and File-Sizing Strategy



\*\*Hackathon Project | Data Engineering\*\*



\---



\## 1. Executive Summary



This project implements and evaluates a time-partitioned data lake using synthetic order data.



The main objective is to design a storage strategy that improves query efficiency, reduces unnecessary file scanning, and controls the small-file problem.



The implementation demonstrates:



\- End-to-end data ingestion and processing.

\- Data validation and transformation.

\- Date-based partitioning using year, month, and day.

\- Parquet file storage.

\- Partition pruning using DuckDB.

\- Daily versus monthly partitioning comparison.

\- Small-file problem simulation and compaction.

\- Output replacement using staging and backup folders.

\- Automated validation tests using Pytest.



The project uses Python, Pandas, PyArrow, DuckDB, and Pytest.



\*\*Key results:\*\*



| Experiment | Result |

|---|---:|

| Synthetic records generated | 100,000 |

| Daily partition files | 30 |

| Monthly partition files | 2 |

| Files scanned for November 11 daily query | 1 of 30 |

| Data read with daily partitioning | 32.7 KB |

| Data read with monthly partitioning | 119.3 KB |

| Files before compaction | 417 |

| Files after compaction | 30 |

| Automated tests passed | 5 |



\---



\## 2. Problem Statement



Design a partitioning and file-sizing strategy for a time-partitioned data lake.



The solution must demonstrate partition pruning, avoid excessive small files, and document trade-offs for common query patterns.



\### Problems addressed



\*\*Problem 1: Inefficient data scanning\*\*



When a dataset contains records from multiple dates, querying one specific date should not require reading every data file.



\*\*Solution:\*\* Organize the data into date-based partitions and demonstrate partition pruning.



\*\*Problem 2: Too many small files\*\*



When data is written in many small files, the query engine must manage additional file metadata and file-opening operations.



\*\*Solution:\*\* Simulate fragmented data and implement compaction to combine small files.



\*\*Problem 3: Choosing the right partition granularity\*\*



Daily partitioning and monthly partitioning have different advantages.



\*\*Solution:\*\* Compare both strategies using the same dataset and the same date-specific query.



\---



\## 3. Understanding the Data Lake Design



A data lake is a storage system used to store large amounts of structured, semi-structured, and unstructured data.



In this project, the data lake stores processed order records in Parquet files.



\### Important concepts



| Concept | Explanation |

|---|---|

| Data lake | Central storage for datasets |

| Partitioning | Dividing data into separate folders based on column values |

| Time partitioning | Organizing data based on date |

| Partition pruning | Skipping partitions that are not required by a query |

| Parquet | Columnar file format used for analytical workloads |

| Small-file problem | Performance and metadata overhead caused by too many small files |

| Compaction | Combining smaller files into fewer larger files |

| Query engine | Software used to read and query stored data |



\---



\## 4. Technology Stack



| Technology | Purpose |

|---|---|

| Python 3.12 | Main programming language |

| Pandas | Data ingestion, validation, and transformation |

| PyArrow | Writing Parquet files |

| DuckDB | Querying Parquet files and examining execution plans |

| Pytest | Automated testing |

| CSV | Raw input data format |

| Parquet | Processed storage format |

| Windows Command Prompt | Project execution environment |



\### Why these technologies?



\- \*\*Python:\*\* Provides a simple way to build and organize the data pipeline.

\- \*\*Pandas:\*\* Makes it easier to load, clean, and transform tabular data.

\- \*\*PyArrow:\*\* Supports efficient Parquet file creation and partitioned output.

\- \*\*DuckDB:\*\* Can query Parquet files directly without requiring a separate database server.

\- \*\*Pytest:\*\* Helps verify that data validation rules work correctly.



This implementation is designed to run locally without requiring a cloud platform or distributed Spark cluster.



\---



\## 5. Dataset Description



The project uses a synthetic order dataset.



\*\*Input file:\*\* `data/raw/orders.csv`



\*\*Number of records:\*\* 100,000



\*\*Number of columns:\*\* 5



\*\*Date range:\*\* October 15, 2026 to November 13, 2026.



\### Dataset schema



| Column | Data type | Description |

|---|---|---|

| order\_id | Integer | Unique order identifier |

| customer\_id | Integer | Customer identifier |

| order\_date | Date | Date on which the order was placed |

| amount | Decimal | Order amount |

| status | String | Order status |



\### Sample records



| order\_id | customer\_id | order\_date | amount | status |

|---:|---:|---|---:|---|

| 100001 | 1250 | 2026-10-15 | 1500.50 | Completed |

| 100002 | 2380 | 2026-10-16 | 2500.00 | Pending |

| 100003 | 3420 | 2026-10-17 | 850.75 | Completed |



\*Illustrative sample records; actual generated values are randomized.\*



The dataset generator uses a fixed random seed so the synthetic dataset can be reproduced.



\---



\## 6. Project Architecture



```text

&#x20;                RAW DATA

&#x20;                   |

&#x20;                   v

&#x20;            orders.csv

&#x20;                   |

&#x20;                   v

&#x20;            DATA INGESTION

&#x20;                   |

&#x20;                   v

&#x20;            DATA VALIDATION

&#x20;                   |

&#x20;             +-----+-----+

&#x20;             |           |

&#x20;             v           v

&#x20;        VALID DATA   REJECTED DATA

&#x20;             |

&#x20;             v

&#x20;       TRANSFORMATION

&#x20;             |

&#x20;             v

&#x20;       DATE EXTRACTION

&#x20;        Year/Month/Day

&#x20;             |

&#x20;             v

&#x20;      DATE PARTITIONING

&#x20;             |

&#x20;             v

&#x20;       PARQUET STORAGE

&#x20;             |

&#x20;      +------+------+----------------+

&#x20;      |             |                |

&#x20;      v             v                v

&#x20;PARTITION       COMPACTION       PARTITION

&#x20; PRUNING        DEMONSTRATION    COMPARISON

&#x20;      |             |                |

&#x20;      v             v                v

&#x20;DUCKDB QUERY   SMALL FILES      DAILY VS

&#x20;               REDUCTION        MONTHLY

```



\### Pipeline explanation



1\. Generate synthetic order data.

2\. Load raw CSV records.

3\. Validate records and separate rejected rows.

4\. Convert columns into suitable data types.

5\. Extract year, month, and day.

6\. Write valid records into date-based Parquet partitions.

7\. Demonstrate partition pruning using DuckDB.

8\. Simulate small files and compact them.

9\. Compare daily and monthly partitioning strategies.



\---



\## 7. Project Folder Structure



```text

data-lake-project/

│

├── data/

│   │

│   ├── raw/

│   │   └── orders.csv

│   │

│   ├── processed/

│   │   ├── orders/

│   │   │   └── year=2026/

│   │   │       └── month=11/

│   │   │           └── day=11/

│   │   │               └── \*.parquet

│   │   │

│   │   └── monthly\_orders/

│   │       └── year=2026/

│   │           └── month=11/

│   │               └── \*.parquet

│   │

│   ├── fragmented/

│   │   └── orders/

│   │

│   └── compacted/

│       └── orders/

│

├── src/

│   ├── data\_generator.py

│   ├── ingestion.py

│   ├── validation.py

│   ├── transformation.py

│   ├── partitioning.py

│   ├── main.py

│   ├── file\_stats.py

│   ├── pruning\_demo.py

│   ├── compaction\_demo.py

│   └── partition\_comparison.py

│

├── tests/

│   └── test\_validation.py

│

├── reports/

│

├── README.md

└── requirements.txt

```



\*Generated data files are created when the scripts run. The folder structure above describes the project's intended organization.\*



\---



\## 8. Implementation Details



\### 8.1 Data Generation



\*\*File:\*\* `src/data\_generator.py`



This script generates 100,000 synthetic order records.



It creates:

\- Unique order IDs.

\- Random customer IDs.

\- Random order dates.

\- Random order amounts.

\- Different order statuses.



The generated data is stored in:



`data/raw/orders.csv`



\*\*Why synthetic data?\*\*



It allows the project to test partitioning, file creation, query performance, and compaction without depending on an external data source.



\### 8.2 Data Ingestion



\*\*File:\*\* `src/ingestion.py`



The ingestion module reads the raw CSV file using Pandas.



Main responsibilities:

\- Check whether the input file exists.

\- Read the CSV data.

\- Display the number of records loaded.

\- Return the loaded DataFrame to the next stage.



\### 8.3 Data Validation



\*\*File:\*\* `src/validation.py`



Validation checks whether records satisfy the implemented data quality rules.



The project checks:



1\. Missing values in any column.

2\. Duplicate order IDs.

3\. Amounts less than or equal to zero.

4\. Status values outside the allowed list.



Allowed statuses:



\- Completed

\- Pending

\- Cancelled



Invalid records are separated from valid records.



The current implementation rejects subsequent occurrences of duplicate order IDs and keeps the first occurrence.



\*\*Why validation matters:\*\*



Invalid data should not continue into the processed data lake because it can affect analytical results.



\### 8.4 Data Transformation



\*\*File:\*\* `src/transformation.py`



The transformation module prepares valid data for storage.



Operations include:

\- Convert `order\_date` to datetime.

\- Convert order and customer IDs into integer types.

\- Convert amount into numeric format.

\- Round amount to two decimal places.

\- Extract year, month, and day from order date.



Example:



| order\_date | year | month | day |

|---|---:|---:|---:|

| 2026-11-11 | 2026 | 11 | 11 |



These date columns are used for partitioning.



\### 8.5 Data Partitioning



\*\*File:\*\* `src/partitioning.py`



The transformed dataset is stored in Parquet format using PyArrow through Pandas.



Partition columns:



\- year

\- month

\- day



Example folder structure:



```text

orders/

&#x20; year=2026/

&#x20;   month=11/

&#x20;     day=10/

&#x20;     day=11/

&#x20;     day=12/

```



Each date has its own partition folder and, in this dataset, one Parquet file.



\#### Why partition by date?



Most time-based analytical queries filter data using dates.



For example:



\- Orders on November 11.

\- Orders during November.

\- Orders during a particular year.



Date-based partitioning makes it possible to skip unrelated date partitions.



\#### Output replacement strategy



The implementation writes new output into a staging directory first.



After writing:

1\. Existing output is moved to a backup directory.

2\. Staging output is promoted to the main output directory.

3\. The backup is removed after successful promotion.

4\. If promotion fails, the code attempts to restore the backup.



This is a safer full-refresh replacement approach, not a fully transactional or concurrent-writer-safe storage system.



\---



\## 9. Partition Pruning Experiment



\*\*File:\*\* `src/pruning\_demo.py`



\### What is partition pruning?



Partition pruning is an optimization technique where the query engine skips partitions that do not match the query conditions.



Without partition pruning, a query may need to inspect many unnecessary files.



With partition pruning, the query engine can use partition column values to narrow down which files need to be read.



\### Example



Suppose the data is stored as:



```text

orders/

&#x20; year=2026/

&#x20;   month=10/

&#x20;     day=15/

&#x20;     day=16/

&#x20;   month=11/

&#x20;     day=10/

&#x20;     day=11/

&#x20;     day=12/

```



If the query requests November 11, the engine does not need to scan October's files or the other November dates.



\### SQL query



```sql

SELECT COUNT(\*)

FROM read\_parquet(

&#x20;   'data/processed/orders/\*\*/\*.parquet',

&#x20;   hive\_partitioning = true

)

WHERE year = 2026

&#x20; AND month = 11

&#x20; AND day = 11;

```



\### Experimental results



| Metric | Result |

|---|---:|

| Total records | 100,000 |

| Matching records | 3,233 |

| Total files | 30 |

| Files scanned | 1 |

| Files skipped | 29 |

| Data read | 32.7 KB |



DuckDB's execution plan reported:



```text

Scanning Files: 1/30

Total Files Read: 1

Data Read: 32.7 kB

```



\### What does this prove?



For the November 11 query, DuckDB scanned one daily partition file instead of all 30 files.



This demonstrates partition pruning in the implemented dataset.



\---



\## 10. Daily vs Monthly Partitioning Experiment



\*\*File:\*\* `src/partition\_comparison.py`



The project compares two partitioning strategies:



\### Daily partitioning



Folder structure:



```text

orders/

&#x20; year=2026/

&#x20;   month=11/

&#x20;     day=10/

&#x20;     day=11/

&#x20;     day=12/

```



Advantages:

\- Better granularity for date-specific queries.

\- Can skip unrelated days.

\- Useful for workloads with frequent daily filters.



Disadvantages:

\- Creates more partition folders.

\- Can produce more files if data volume is very small.



\### Monthly partitioning



Folder structure:



```text

monthly\_orders/

&#x20; year=2026/

&#x20;   month=10/

&#x20;   month=11/

```



Advantages:

\- Fewer partitions.

\- Useful for month-level queries.

\- Simpler organization for monthly reporting.



Disadvantages:

\- A daily query may need to inspect data inside a larger monthly file.

\- May read more data for date-specific queries.



\### Comparison results



Both strategies were tested using the same November 11 query.



| Metric | Daily | Monthly |

|---|---:|---:|

| Total files | 30 | 2 |

| Files scanned | 1 | 1 |

| Records returned | 3,233 | 3,233 |

| Data read | 32.7 KB | 119.3 KB |



\### Interpretation



Both strategies returned the same 3,233 records.



However:

\- Daily partitioning read 32.7 KB.

\- Monthly partitioning read 119.3 KB.



DuckDB's monthly execution plan also reported row-group filtering within the selected monthly file.



\### Final decision



Daily partitioning was selected for the main dataset because the demonstrated workload focuses on date-specific queries.



Monthly partitioning remains a useful alternative when queries primarily access full months and reducing partition count is important.



The results are from a local synthetic dataset and one execution-plan comparison, not a universal performance benchmark.



\---



\## 11. Small-File Problem



\### What is the small-file problem?



A small-file problem occurs when a data lake contains a large number of small files instead of a manageable number of larger files.



For example:



```text

orders/

&#x20; part1.parquet

&#x20; part2.parquet

&#x20; part3.parquet

&#x20; part4.parquet

&#x20; part5.parquet

&#x20; ...

```



A large number of files can increase:

\- File-opening overhead.

\- Metadata management.

\- Query planning work.

\- Storage management complexity.



\### Why does it happen?



It can happen when:

\- Data arrives in small batches.

\- Frequent pipeline runs create separate files.

\- Multiple writers produce small outputs.

\- Partitioned datasets have low data volume per partition.



\### How did this project demonstrate it?



\*\*File:\*\* `src/compaction\_demo.py`



The script deliberately divides daily data into smaller chunks of 250 rows.



Each chunk is written as a separate Parquet file.



This creates a fragmented dataset for the experiment.



\---



\## 12. File Compaction Implementation



\### What is compaction?



Compaction is the process of combining multiple small files into fewer, larger files.



The project:

1\. Reads the original daily partitioned dataset.

2\. Splits the records into small chunks.

3\. Writes the chunks into a fragmented directory.

4\. Reads the fragmented files for each date.

5\. Combines the records belonging to the same date.

6\. Writes the combined records into the compacted directory.

7\. Compares file counts, sizes, and record counts.



The original date-based partition structure is preserved.



\### Compaction results



| Metric | Before | After |

|---|---:|---:|

| Parquet files | 417 | 30 |

| Total size | 3,143.14 KB | 1,779.68 KB |

| Records | 100,000 | 100,000 |



\*\*Files removed:\*\* 387



\*\*File count reduction:\*\* Approximately 92.8%.



\*\*Record counts:\*\* Matched before and after compaction.



\### What does this prove?



The experiment demonstrates that multiple small files can be combined into fewer files while retaining the same total number of records.



The current experiment checks record counts, not full row-by-row equality.



The 250-row chunk size is used only to simulate fragmentation. It is not a production file-size target.



\---



\## 13. File Size Analysis



\*\*File:\*\* `src/file\_stats.py`



The script examines the original daily Parquet dataset.



\### Results



| Metric | Result |

|---|---:|

| Total files | 30 |

| Total size | 1,933.08 KB |

| Smallest file | 62.61 KB |

| Largest file | 66.63 KB |

| Average file size | 64.44 KB |



\### Production consideration



A common initial target for analytical Parquet files is around 128–512 MB, although the ideal size depends on the query engine, storage system, workload, and partition distribution.



The files in this project are much smaller because the dataset contains only 100,000 synthetic records stored locally.



The goal of this project is to demonstrate the file-sizing strategy, not to claim production-scale file sizes.



\---



\## 14. Automated Testing



\*\*File:\*\* `tests/test\_validation.py`



Pytest is used to verify the validation logic.



The project contains five test cases:



| Test | Purpose |

|---|---|

| Mixed valid and invalid records | Check separation of valid and rejected rows |

| Duplicate order IDs | Verify duplicate rejection |

| Missing values | Verify records with null values are rejected |

| Negative amounts | Verify invalid amounts are rejected |

| Invalid statuses | Verify unsupported statuses are rejected |



\### Test command



```cmd

python -m pytest tests\\test\_validation.py -v

```



\### Result



```text

5 passed

```



The tests verify the implemented validation rules using sample DataFrames.



\---



\## 15. How to Set Up and Run the Project



\### Prerequisites



Install:

\- Python 3.12

\- pip



\### Step 1: Create and activate a virtual environment



```cmd

python -m venv venv

venv\\Scripts\\activate

```



\### Step 2: Install dependencies



```cmd

pip install pandas pyarrow duckdb pytest

```



\### Step 3: Generate the synthetic dataset



```cmd

python src\\data\_generator.py

```



\### Step 4: Run the main pipeline



```cmd

python src\\main.py

```



\### Step 5: Check file statistics



```cmd

python src\\file\_stats.py

```



\### Step 6: Demonstrate partition pruning



```cmd

python src\\pruning\_demo.py

```



\### Step 7: Demonstrate compaction



```cmd

python src\\compaction\_demo.py

```



\### Step 8: Compare daily and monthly partitioning



```cmd

python src\\partition\_comparison.py

```



\### Step 9: Run automated tests



```cmd

python -m pytest tests\\test\_validation.py -v

```



\---



\## 16. Important Design Decisions



| Decision | Reason |

|---|---|

| Use synthetic order data | Reproducible testing without an external source |

| Use date-based partitions | Support time-based queries |

| Choose daily partitioning | Better result for the tested daily query |

| Use Parquet | Columnar storage suitable for analytical queries |

| Use DuckDB | Query Parquet files directly and inspect execution plans |

| Simulate fragmentation | Demonstrate the small-file problem |

| Implement compaction | Reduce file count while preserving record counts |

| Use staging and backup | Make full-refresh output replacement safer |



\---



\## 17. Current Scope and Limitations



This implementation is a local proof of concept using a 100,000-row synthetic dataset.



The following are not implemented:



\- Cloud object storage integration.

\- Distributed processing with Spark.

\- Incremental or CDC ingestion.

\- Production scheduling and orchestration.

\- Persistent rejected-record storage.

\- Centralized monitoring and logging.

\- Schema evolution management.

\- Concurrent writer coordination.

\- Production-scale file-size benchmarking.

\- Full row-by-row data reconciliation after compaction.



These are potential extensions for a production implementation.



\---



\## 18. Future Improvements



Possible next improvements include:



1\. Add incremental ingestion so only new records are processed.

2\. Store rejected records in a dedicated location.

3\. Add run metadata, execution status, and error logs.

4\. Implement automated compaction based on file count or file size.

5\. Add full data reconciliation using unique order IDs and content comparisons.

6\. Integrate cloud storage such as Amazon S3 or Azure Data Lake.

7\. Use Apache Spark for larger datasets.

8\. Add scheduled pipeline execution and monitoring.



\---



\## 19. Final Conclusion



This project demonstrates a practical approach to designing a time-partitioned data lake.



The implementation covers the complete local processing flow from raw CSV ingestion to partitioned Parquet storage.



The experiments demonstrate:



\- Date-based data organization.

\- Partition pruning using DuckDB.

\- Daily and monthly partitioning trade-offs.

\- Small-file fragmentation.

\- Compaction to reduce file count.

\- Automated validation testing.



Based on the tested date-specific query, daily partitioning was selected for the main dataset because it read less data than monthly partitioning.



The compaction experiment reduced the file count from 417 to 30 while preserving the total record count.



The project provides a foundation for extending the solution to larger datasets and production data engineering environments.



\---



\*\*Project Focus:\*\* Data Lake Design | Partitioning Strategy | Partition Pruning | Parquet | File Compaction | Data Engineering



