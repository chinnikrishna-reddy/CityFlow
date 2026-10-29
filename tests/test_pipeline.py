
from pathlib import Path
import subprocess
import sys
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent


def test_pipeline_outputs():
    result = subprocess.run(
        [sys.executable, str(BASE_DIR / "src" / "pipeline.py")],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr

    clean_file = BASE_DIR / "data" / "processed" / "traffic_incidents.parquet"
    rejected_file = BASE_DIR / "data" / "rejected" / "rejected_incidents.csv"

    assert clean_file.exists()
    assert rejected_file.exists()

    clean = pd.read_parquet(clean_file)
    rejected = pd.read_csv(rejected_file)

    assert len(clean) == 10
    assert len(rejected) == 1
    assert clean["incident_id"].is_unique
    assert clean["severity"].isin(["Low", "Medium", "High"]).all()
    assert clean["vehicles_involved"].ge(0).all()
    assert rejected["rejection_reason"].notna().all()
