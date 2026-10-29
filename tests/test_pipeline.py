
from pathlib import Path
import subprocess
import sys

import pandas as pd
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def pipeline_data():
    result = subprocess.run(
        [sys.executable, str(BASE_DIR / "src" / "pipeline.py")],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr

    clean_file = (
        BASE_DIR / "data" / "processed" / "traffic_incidents.parquet"
    )
    rejected_file = (
        BASE_DIR / "data" / "rejected" / "rejected_incidents.csv"
    )

    assert clean_file.exists()
    assert rejected_file.exists()

    clean = pd.read_parquet(clean_file)
    rejected = pd.read_csv(rejected_file)

    return clean, rejected


def test_pipeline_outputs_exist(pipeline_data):
    clean, rejected = pipeline_data

    assert not clean.empty
    assert clean is not None
    assert rejected is not None


def test_expected_record_counts(pipeline_data):
    clean, rejected = pipeline_data

    assert len(clean) == 10
    assert len(rejected) == 1


def test_incident_ids_are_unique(pipeline_data):
    clean, _ = pipeline_data

    assert clean["incident_id"].is_unique


def test_clean_records_have_valid_values(pipeline_data):
    clean, _ = pipeline_data

    assert clean["severity"].isin(
        ["Low", "Medium", "High"]
    ).all()

    assert clean["vehicles_involved"].ge(0).all()

    assert clean["incident_id"].notna().all()
    assert clean["city"].notna().all()
    assert clean["state"].notna().all()


def test_no_exact_duplicate_rows(pipeline_data):
    clean, _ = pipeline_data

    assert not clean.duplicated().any()


def test_rejected_records_have_reasons(pipeline_data):
    _, rejected = pipeline_data

    assert "rejection_reason" in rejected.columns
    assert rejected["rejection_reason"].notna().all()
    assert rejected["rejection_reason"].astype(str).str.strip().ne("").all()
