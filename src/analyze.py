
from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parent.parent
PARQUET_FILE = BASE_DIR / "data" / "processed" / "traffic_incidents.parquet"

con = duckdb.connect()

print("\nINCIDENTS BY CITY")
print(con.execute("""
    SELECT city, COUNT(*) AS total_incidents
    FROM read_parquet(?)
    GROUP BY city
    ORDER BY total_incidents DESC
""", [str(PARQUET_FILE)]).df().to_string(index=False))

print("\nINCIDENTS BY SEVERITY")
print(con.execute("""
    SELECT severity, COUNT(*) AS total_incidents
    FROM read_parquet(?)
    GROUP BY severity
    ORDER BY total_incidents DESC
""", [str(PARQUET_FILE)]).df().to_string(index=False))

print("\nINCIDENTS BY STATE")
print(con.execute("""
    SELECT state, COUNT(*) AS total_incidents
    FROM read_parquet(?)
    GROUP BY state
    ORDER BY total_incidents DESC
""", [str(PARQUET_FILE)]).df().to_string(index=False))

con.close()
