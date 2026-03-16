CREATE DATABASE IF NOT EXISTS aurora;
USE aurora;

CREATE TABLE IF NOT EXISTS metrics_funnel_daily (
  dt DATE PRIMARY KEY,
  sessions_total BIGINT,
  sessions_event_list BIGINT,
  sessions_event_detail BIGINT,
  sessions_begin_checkout BIGINT,
  sessions_purchase BIGINT,
  conversion_rate DECIMAL(10,4)
);

CREATE TABLE IF NOT EXISTS metrics_event_rank (
  dt DATE,
  event_id INT,
  name VARCHAR(255),
  detail_views BIGINT,
  purchases BIGINT,
  revenue_total DECIMAL(12,2),
  interest_to_purchase_ratio DECIMAL(12,4),
  PRIMARY KEY (dt, event_id)
);

CREATE TABLE IF NOT EXISTS metrics_anomalies (
  dt DATE,
  dimension VARCHAR(64),
  ip VARCHAR(64),
  page VARCHAR(255),
  requests BIGINT,
  errors BIGINT,
  purchases BIGINT,
  is_anomaly BOOLEAN,
  reason VARCHAR(255),
  PRIMARY KEY (dt, dimension, ip, page(120))
);
