{{ config(materialized="table") }}

with trip_durations as (
    select
        year,
        month,
        pickup_locationid,
        dropoff_locationid,
        pickup_zone,
        dropoff_zone,
        TIMESTAMP_DIFF(dropoff_datetime , pickup_datetime , second) AS trip_duration,
    from {{ ref("fact_fhv_trips") }}
    where pickup_zone in ('Newark Airport', 'SoHo','Yorkville East')
    and year = 2019 
    and month = 11
),
zone_percentiles as (
    select
        pickup_zone,
        dropoff_zone,
        PERCENTILE_CONT(trip_duration, 0.9) OVER(partition by year, month, pickup_locationid, dropoff_locationid) AS trip_duration_p90,
    from trip_durations
),
percentile_ranks as (
    select
        pickup_zone,
        dropoff_zone,
        trip_duration_p90,
        DENSE_RANK() over(partition by pickup_zone order by trip_duration_p90 desc) as perc_rank,
    from zone_percentiles
),
deduplicate_ranks as (
    select
        *,
        ROW_NUMBER() OVER (PARTITION BY pickup_zone) AS row_num
    from percentile_ranks
    where perc_rank=2
)
select
    pickup_zone,
    dropoff_zone,
    trip_duration_p90
from deduplicate_ranks
where row_num = 1
