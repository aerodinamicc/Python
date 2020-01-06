WITH src as (
select 
  first_value(tags) OVER (PARTITION BY link
                    ORDER BY visited_timestamp) as tags,
  first_value(url_extract_host(link)) OVER (PARTITION BY link
                    ORDER BY visited_timestamp) as host,
  first_value(views) OVER (PARTITION BY link
                    ORDER BY visited_timestamp) as views,
  first_value(comments) OVER (PARTITION BY link
                    ORDER BY visited_timestamp) as comments
  
from raw
where tags IS NOT NULL AND tags <> ''
  )

select
lower(tag),
count(*) as tag_count,
round(avg(comments)) as avg_comments,
round(avg(views)) as avg_view 
from src
cross join unnest(split(tags, ' - ')) as t(tag)
group by 1
order by 2 desc

