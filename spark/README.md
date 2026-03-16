# Spark Jobs

This folder contains the two mandatory Spark 3.5 jobs required by the PDF.

- `jobs/01_curate_raw_to_curated.py`: reads raw clickstream JSONL and raw business CSVs, cleans them, and writes partitioned Parquet to `curated/`.
- `jobs/02_curated_to_analytics.py`: reads `curated/`, computes the three mandatory products, writes Parquet to `analytics/`, and optionally loads final metrics to MySQL.

Example submit commands:

```bash
spark-submit \
  --master spark://<spark-master-private-ip>:7077 \
  spark/jobs/01_curate_raw_to_curated.py \
  --student-id "$STUDENT_ID" \
  --raw-clickstream "s3a://$S3_BUCKET/$RAW_PREFIX/clickstream/*.jsonl" \
  --raw-events "s3a://$S3_BUCKET/$RAW_PREFIX/business/events.csv" \
  --raw-campaigns "s3a://$S3_BUCKET/$RAW_PREFIX/business/campaigns.csv" \
  --raw-transactions "s3a://$S3_BUCKET/$RAW_PREFIX/business/transactions.csv" \
  --curated-base "s3a://$S3_BUCKET/$CURATED_PREFIX"
```

```bash
spark-submit \
  --master spark://<spark-master-private-ip>:7077 \
  --jars /opt/spark/jars/mysql-connector-j-8.4.0.jar \
  spark/jobs/02_curated_to_analytics.py \
  --student-id "$STUDENT_ID" \
  --curated-base "s3a://$S3_BUCKET/$CURATED_PREFIX" \
  --analytics-base "s3a://$S3_BUCKET/$ANALYTICS_PREFIX" \
  --mysql-url "jdbc:mysql://$RDS_HOST:$RDS_PORT/$RDS_DATABASE" \
  --mysql-user "$RDS_USER" \
  --mysql-password "$RDS_PASSWORD"
```
