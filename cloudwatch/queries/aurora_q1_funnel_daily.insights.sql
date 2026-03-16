fields @timestamp, dt, event_type, session_id
| filter source = "client"
| stats
    count_distinct(session_id) as sessions_total,
    count_distinct(if(event_type="view_event_list", session_id, null)) as sessions_event_list,
    count_distinct(if(event_type="view_event_detail", session_id, null)) as sessions_event_detail,
    count_distinct(if(event_type="begin_checkout", session_id, null)) as sessions_begin_checkout,
    count_distinct(if(event_type="purchase", session_id, null)) as sessions_purchase
  by dt
| sort dt asc
