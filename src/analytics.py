
from pathlib import Path

import duckdb

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "processed" / "traffic_incidents.parquet"


def get_incidents_by_severity():
    query = """
    SELECT
        severity,
        COUNT(*) AS total_incidents
    FROM read_parquet(?)
    GROUP BY severity
    ORDER BY total_incidents DESC
    """

    with duckdb.connect(database=":memory:") as connection:
        return connection.execute(
            query, [str(DATA_FILE)]
        ).df()


def get_top_cities(limit=10):
    query = """
    SELECT
        state,
        city,
        COUNT(*) AS total_incidents
    FROM read_parquet(?)
    GROUP BY state, city
    ORDER BY total_incidents DESC, state, city
    LIMIT ?
    """

    with duckdb.connect(database=":memory:") as connection:
        return connection.execute(
            query, [str(DATA_FILE), limit]
        ).df()


if __name__ == "__main__":
    print("\nIncidents by Severity")
    print(get_incidents_by_severity().to_string(index=False))

    print("\nTop 10 Cities")
    print(get_top_cities().to_string(index=False))
