
-- 1. Count incidents by city
SELECT city, COUNT(*) AS total_incidents
FROM read_parquet('data/processed/traffic_incidents.parquet')
GROUP BY city
ORDER BY total_incidents DESC;

-- 2. Count incidents by severity
SELECT severity, COUNT(*) AS total_incidents
FROM read_parquet('data/processed/traffic_incidents.parquet')
GROUP BY severity
ORDER BY total_incidents DESC;

-- 3. Count incidents by state
SELECT state, COUNT(*) AS total_incidents
FROM read_parquet('data/processed/traffic_incidents.parquet')
GROUP BY state
ORDER BY total_incidents DESC;

