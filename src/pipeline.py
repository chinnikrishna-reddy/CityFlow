
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "raw" / "traffic_incidents.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
REJECTED_DIR = BASE_DIR / "data" / "rejected"

VALID_SEVERITIES = {"Low", "Medium", "High"}
REQUIRED_COLUMNS = [
    "incident_id",
    "state",
    "city",
    "incident_type",
    "severity",
    "incident_time",
    "vehicles_involved",
]


def run_pipeline():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    REJECTED_DIR.mkdir(parents=True, exist_ok=True)

    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE)
    df.columns = df.columns.str.strip()

    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing columns: {sorted(missing_columns)}")

    original_count = len(df)

    df = df.drop_duplicates()
    df["incident_time"] = pd.to_datetime(
        df["incident_time"], errors="coerce"
    )
    df["vehicles_involved"] = pd.to_numeric(
        df["vehicles_involved"], errors="coerce"
    )

    valid = (
        df["incident_id"].notna()
        & df["incident_id"].astype(str).str.strip().ne("")
        & df["state"].notna()
        & df["city"].notna()
        & df["incident_type"].isin(
            ["Collision", "Congestion", "Road Hazard"]
        )
        & df["severity"].isin(VALID_SEVERITIES)
        & df["incident_time"].notna()
        & df["vehicles_involved"].notna()
        & df["vehicles_involved"].ge(0)
        & df["vehicles_involved"].mod(1).eq(0)
    )

    rejected = df.loc[~valid].copy()
    rejected["rejection_reason"] = "One or more validation rules failed"

    clean = df.loc[valid].copy()
    clean["vehicles_involved"] = clean["vehicles_involved"].astype(int)
    clean["incident_date"] = clean["incident_time"].dt.date.astype(str)

    clean_path = PROCESSED_DIR / "traffic_incidents.parquet"
    rejected_path = REJECTED_DIR / "rejected_incidents.csv"

    clean.to_parquet(clean_path, index=False)
    rejected.to_csv(rejected_path, index=False)

    print("CITYFLOW PIPELINE COMPLETED")
    print(f"Input records: {original_count}")
    print(f"Records after duplicate removal: {len(df)}")
    print(f"Clean records: {len(clean)}")
    print(f"Rejected records: {len(rejected)}")
    print(f"Clean output: {clean_path}")
    print(f"Rejected output: {rejected_path}")


if __name__ == "__main__":
    run_pipeline()
