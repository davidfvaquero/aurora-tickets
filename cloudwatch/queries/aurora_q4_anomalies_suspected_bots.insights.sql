fields dt, ip, page, event_type, status_code
| stats
    count(*) as requests,
    count(if(status_code >= 400, 1, null)) as errors,
    count_distinct(session_id) as sessions,
    count(if(event_type="purchase", 1, null)) as purchases
  by dt, ip, page
| filter requests >= 80 or errors >= 8 or (requests >= 50 and purchases = 0)
| sort requests desc, errors desc
