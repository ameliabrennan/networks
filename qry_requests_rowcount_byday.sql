SELECT timestamp_day, count(distinct(id)) as request_count_by_day
FROM requests 
GROUP BY timestamp_day 
ORDER BY timestamp_day;