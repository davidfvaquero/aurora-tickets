# Evaluation

## Validation checks

- `sessions_purchase <= sessions_begin_checkout <= sessions_total`
- Revenue is non-negative.
- Anomaly rules are explainable and reproducible.
- Partitioned Parquet exists in both `curated/` and `analytics/`.

## Risks and assumptions

- Some bot behavior is synthetic, so thresholds should be explained as heuristic.
- Campaign attribution is simplified to UTM matching.
- Transactions represent completed purchase facts, not payment processing detail.
