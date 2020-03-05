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

-----------------------
--- Daily popularity of different tags (ordered by views and comments)
-----------------------
 
WITH src as (
select
  link,
  title,
  views,
  comments,
  date_parse(visited_timestamp, '%Y-%m-%d %H:%i:%S') as visited_timestamp,
  date_parse(created_timestamp, '%Y-%m-%d %H:%i:%S') as created_timestamp,
  lag(comments) OVER (PARTITION BY link
                    ORDER BY visited_timestamp) as prev_comments,
  lag(views) OVER (PARTITION BY link
                    ORDER BY visited_timestamp) as prev_views,
  lag(date_parse(visited_timestamp, '%Y-%m-%d %H:%i:%S')) OVER (PARTITION BY link
                    ORDER BY visited_timestamp) as prev_visited,
  tags,
  category,
  
  row_number() OVER (PARTITION BY link
                    ORDER BY visited_timestamp) as rnk
  from news.raw
  where substr(created_timestamp, 1, 10) like '2020-%'
  and url_extract_host(link) like '%news.bg'
),
  
daily as (select 
  date(visited_timestamp) as date,
  split(lower(tags), ' - ') as tags,
case when rnk = 1 then comments
     else comments - prev_comments END AS comments_generated,
case when rnk = 1 then views
     else views - prev_views END AS views_generated
from src),

elongated as (select date, tag, sum(comments_generated) as sum_comments, sum(views_generated) as sum_views
from daily
cross join unnest(tags) as t(tag)
group by 1, 2
order by 1, 2)

select date, tag, sum_comments, sum_views, row_number() over (partition by date order by sum_views desc, sum_comments desc) as rank
from elongated
-- where sum_views > 10000
-- where regexp_like(tag, '(?:(?:^евро$)|еврозона)')
order by 1, 4 desc, 3 desc

