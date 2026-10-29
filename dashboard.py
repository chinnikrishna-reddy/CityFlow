
from pathlib import Path

import duckdb
import pandas as pd
import streamlit as st
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from analytics import get_incidents_by_severity, get_top_cities

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "processed" / "traffic_incidents.parquet"

st.set_page_config(
    page_title="CityFlow | Traffic Analytics",
    page_icon="🚦",
    layout="wide"
)

st.title("🚦 CityFlow Traffic Analytics")
st.caption("Explore and analyze traffic incident records")

if not DATA_FILE.exists():
    st.error("Processed data not found. Run the ETL pipeline first.")
    st.code(r".\.venv\Scripts\python.exe src\pipeline.py")
    st.stop()

try:
    con = duckdb.connect(database=":memory:")
    df = con.execute(
        "SELECT * FROM read_parquet(?)",
        [str(DATA_FILE)]
    ).df()
    con.close()
except Exception as error:
    st.error(f"Unable to load the data: {error}")
    st.stop()

if df.empty:
    st.warning("No clean traffic incident records are available.")
    st.stop()

st.sidebar.header("Filters")

states = sorted(df["state"].dropna().unique().tolist())
selected_states = st.sidebar.multiselect(
    "Select states",
    states,
    default=states
)

severities = sorted(df["severity"].dropna().unique().tolist())
selected_severities = st.sidebar.multiselect(
    "Select severity",
    severities,
    default=severities
)

incident_types = sorted(
    df["incident_type"].dropna().unique().tolist()
)
selected_types = st.sidebar.multiselect(
    "Select incident types",
    incident_types,
    default=incident_types
)

filtered_df = df[
    df["state"].isin(selected_states)
    & df["severity"].isin(selected_severities)
    & df["incident_type"].isin(selected_types)
]

total_incidents = len(filtered_df)
high_severity = int(
    (filtered_df["severity"] == "High").sum()
)
total_vehicles = int(
    filtered_df["vehicles_involved"].sum()
)
cities_affected = filtered_df["city"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Incidents", total_incidents)
col2.metric("High Severity", high_severity)
col3.metric("Vehicles Involved", total_vehicles)
col4.metric("Cities Affected", cities_affected)

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Incidents by Severity")
    severity_counts = (
        filtered_df["severity"]
        .value_counts()
        .reindex(["Low", "Medium", "High"], fill_value=0)
    )
    st.bar_chart(severity_counts)

with right:
    st.subheader("Incidents by Type")
    type_counts = filtered_df["incident_type"].value_counts()
    st.bar_chart(type_counts)

st.subheader("Incidents by State")

state_counts = (
    filtered_df.groupby("state")
    .size()
    .sort_values(ascending=False)
)
st.bar_chart(state_counts)

st.subheader("Incident Records")

display_columns = [
    "incident_id",
    "state",
    "city",
    "incident_type",
    "severity",
    "incident_time",
    "vehicles_involved"
]

available_columns = [
    column for column in display_columns
    if column in filtered_df.columns
]

st.dataframe(
    filtered_df[available_columns],
    use_container_width=True,
    hide_index=True
)

csv_data = filtered_df[available_columns].to_csv(index=False)

st.download_button(
    label="Download filtered incidents as CSV",
    data=csv_data,
    file_name="cityflow_incidents.csv",
    mime="text/csv"
)

st.caption(
    "Data disclaimer: The initial dataset contains synthetic "
    "demonstration records and does not represent actual Indian "
    "traffic statistics."
)

st.divider()

st.header("SQL Analytics")

st.subheader("Incident Summary by Severity")
severity_summary = get_incidents_by_severity()
st.dataframe(severity_summary, width="stretch", hide_index=True)

st.subheader("Top 10 Cities by Incidents")
top_cities = get_top_cities()
st.dataframe(top_cities, use_container_width=True, hide_index=True)

