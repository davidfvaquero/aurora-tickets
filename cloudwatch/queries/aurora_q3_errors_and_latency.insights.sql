fields dt, request_path, status_code, latency_ms
| filter source = "server"
| stats
    count(*) as requests,
    count(if(status_code >= 400, 1, null)) as errors,
    avg(latency_ms) as avg_latency_ms,
    pct(latency_ms, 95) as p95_latency_ms
  by dt, request_path
| sort dt desc, errors desc, p95_latency_ms desc
