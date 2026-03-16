# Data Preparation

## Cleaning rules

- Reject malformed timestamps.
- Cast numeric columns and filter impossible values.
- Remove empty IDs and duplicate transaction IDs.
- Keep only reasonable ranges for prices, quantities, and capacities.
- Normalize `utm_campaign` empty strings to null.

## Curated layer

Outputs are written as Parquet in S3 under `curated/` with mandatory partitioning:

- Clickstream: `dt`, `source`
- Transactions: `dt`, `payment_method`
- Events: `category`
- Campaigns: `channel`

## Why these rules

The goal is to preserve analytical usefulness while removing deliberate noise from the generated source data.
