# Data Understanding

## Sources

- Clickstream JSONL produced by the Aurora web application.
- `events.csv`, `campaigns.csv`, `transactions.csv` generated with intentional data quality issues.
- CloudWatch operational logs derived from the same clickstream file.

## Join keys

- `event_id`: clickstream, events, transactions.
- `utm_campaign`: clickstream, campaigns.
- `session_id`: clickstream, transactions.

## Expected temporal shape

The simulation covers 7 days and produces at least 200,000 events through a mix of direct replay and real HTTP traffic.

## Data quality issues expected

- Nulls and malformed values.
- Outliers in price and amount.
- Orphan foreign keys.
- Inconsistent types.
- Dates outside the expected range or not parseable.
