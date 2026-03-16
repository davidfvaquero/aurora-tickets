fields dt, event_type, event_id, amount
| filter source = "client" and ispresent(event_id)
| stats
    count(if(event_type="view_event_detail", 1, null)) as detail_views,
    count(if(event_type="purchase", 1, null)) as purchases,
    sum(if(event_type="purchase", amount, 0)) as revenue_total
  by dt, event_id
| sort revenue_total desc, detail_views desc
