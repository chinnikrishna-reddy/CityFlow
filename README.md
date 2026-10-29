# CityFlow — Traffic Incident Data Pipeline

CityFlow is a beginner-built data engineering project that demonstrates how traffic incident records can be ingested, validated, cleaned, stored in Parquet format, and analyzed using SQL.

## Current Features

- CSV data ingestion using Python and pandas
- Duplicate removal and data-quality validation
- Rejected-record tracking with rejection reasons
- Clean data storage in Parquet format
- SQL analytics using DuckDB
- Automated pipeline checks using pytest

## Technology Stack

- Python
- pandas
- PyArrow
- DuckDB
- SQL
- pytest

## Project Structure

```text
CityFlow/
├── data/
│   ├── raw/
│   ├── processed/
│   └── rejected/
├── src/
│   ├── pipeline.py
│   └── analyze.py
├── sql/
│   └── analytics.sql
├── tests/
│   └── test_pipeline.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

Install Python, then create and activate a virtual environment.

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run the Pipeline

```powershell
.\.venv\Scripts\python.exe src\pipeline.py
```

## Run Analytics

```powershell
.\.venv\Scripts\python.exe src\analyze.py
```

## Run Tests

```powershell
.\.venv\Scripts\python.exe -m pytest tests -v
```

## Data Disclaimer

The initial CSV contains synthetic demonstration records. Its analysis does not represent actual Indian traffic statistics. Integration with an authentic Indian road-accident or traffic dataset is planned as a subsequent development step.

## Future Improvements

- Integrate an authentic Indian government road-safety dataset
- Add incremental processing and pipeline run logs
- Track data freshness and processing failures
- Add a dashboard for traffic incident analytics
- Automate testing using GitHub Actions

## Project Status

Initial ETL pipeline and SQL analytics implemented. Automated tests and documentation are being developed.
