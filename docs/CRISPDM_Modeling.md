# Modeling

## Architecture

- EC2-1: Spark Master
- EC2-2/3/4: Spark Workers
- EC2-5: submit node
- EC2-6: web + FastAPI + CloudWatch Agent
- S3: `raw/`, `curated/`, `analytics/`
- RDS MySQL: final metrics only
- CloudWatch: log group, saved queries, dashboard

## Spark jobs

- Job 1 curates raw clickstream and business CSVs into typed partitioned Parquet.
- Job 2 builds the mandatory analytical products and pushes the final tables to MySQL.

## Analytical products

- Funnel conversion daily.
- Event ranking by interest versus revenue.
- Rule-based anomaly detection on request volume, errors, and purchase absence.
