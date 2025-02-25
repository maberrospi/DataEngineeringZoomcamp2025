{{ config(materialized="table") }}

with percentile_table as (
    select
        service_type,
        PERCENTILE_CONT(fare_amount, 0.9) OVER(partition by service_type, year, month) AS perc90,
        PERCENTILE_CONT(fare_amount, 0.95) OVER(partition by service_type, year, month) AS perc95,
        PERCENTILE_CONT(fare_amount, 0.97) OVER(partition by service_type, year, month) AS perc97
    from {{ ref("fact_trips") }}
    where fare_amount>0 and trip_distance>0 and payment_type_description in ('Cash', 'Credit card')
    and year = 2020 
    and month = 4
)
select 
    service_type,
    MAX(perc90) AS perc90,
    MAX(perc95) AS perc95,
    MAX(perc97) AS perc97
from percentile_table
group by service_type
