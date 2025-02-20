{{ config(materialized="table") }}

with quarterly_revenues as (
    select
        service_type,
        year,
        quarter,
        year_quarter,
        -- month,
        -- total_amount,
        sum(total_amount) as quarter_revenue
    from {{ ref("fact_trips") }}
    group by service_type,year,quarter,year_quarter
    order by year desc,quarter asc
),

-- select * from quarterly_revenues
previous_year_quarter as(
    select
        *,
        LAG(year,4) over (partition by service_type order by year,quarter) as prev_year,
        LAG(quarter,4) over (partition by service_type order by year,quarter) as prev_quarter,
        LAG(year_quarter,4) over (partition by service_type order by year,quarter) as prev_year_quarter,
        LAG(quarter_revenue,4) over (partition by service_type order by year,quarter) as prev_quarter_revenue
    from quarterly_revenues
),
yoy_revenue_growths as (
select
    service_type,
    year_quarter,
    prev_year_quarter,
    quarter_revenue,
    prev_quarter_revenue,
    case when year = prev_year+1 and quarter=prev_quarter
        then 100 * ((quarter_revenue-prev_quarter_revenue)/nullif(prev_quarter_revenue,0)) 
    else null
    end as yoy_revenue_growth

from previous_year_quarter
)
select * from yoy_revenue_growths
where yoy_revenue_growth is not null

