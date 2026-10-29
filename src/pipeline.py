
import logging
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "raw" / "traffic_incidents.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
REJECTED_DIR = BASE_DIR / "data" / "rejected"
LOG_FILE = BASE_DIR / "data" / "pipeline.log"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REJECTED_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding="utf-8")
    ],
    force=True
)

logger = logging.getLogger(__name__)

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
    logger.info("Pipeline started")

    if not INPUT_FILE.exists():
        logger.error("Input file not found: %s", INPUT_FILE)
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE)
    df.columns = df.columns.str.strip()

    original_count = len(df)
    logger.info("Input records: %d", original_count)

    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing_columns:
        logger.error("Missing columns: %s", sorted(missing_columns))
        raise ValueError(f"Missing columns: {sorted(missing_columns)}")

    df = df.drop_duplicates()

    logger.info("Duplicate removal completed")
    logger.info("Records after duplicate removal: %d", len(df))

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
        & df["state"].astype(str).str.strip().ne("")
        & df["city"].notna()
        & df["city"].astype(str).str.strip().ne("")
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
    rejected["rejection_reason"] = (
        "One or more validation rules failed"
    )

    clean = df.loc[valid].copy()

    clean["vehicles_involved"] = (
        clean["vehicles_involved"].astype(int)
    )

    clean["incident_date"] = (
        clean["incident_time"].dt.date.astype(str)
    )

    logger.info("Clean records: %d", len(clean))
    logger.info("Rejected records: %d", len(rejected))

    clean_path = PROCESSED_DIR / "traffic_incidents.parquet"
    rejected_path = REJECTED_DIR / "rejected_incidents.csv"

    clean.to_parquet(clean_path, index=False)
    rejected.to_csv(rejected_path, index=False)

    logger.info("Clean output saved: %s", clean_path)
    logger.info("Rejected output saved: %s", rejected_path)
    logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception:
        logger.exception("Pipeline failed")
        raise
