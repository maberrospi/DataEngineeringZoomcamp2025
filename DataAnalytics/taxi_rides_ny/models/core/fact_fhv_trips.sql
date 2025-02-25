{{config(materialized='table')}}

with fhv_data as (
    select
        *,
        'Fhv' as service_type
    from {{ref("stg_fhv_tripdata")}}
),
dim_zones as (
    select * from {{ref("dim_zones")}}
    where borough != 'Unknown'
)
select 
    fhv_data.dispatching_base_num,
    fhv_data.service_type,
    fhv_data.pickup_locationid,
    zoned_pickup_zone.borough as pickup_borough,
    zoned_pickup_zone.zone as pickup_zone,
    fhv_data.dropoff_locationid,
    zones_dropoff_zone.borough as dropoff_borough,
    zones_dropoff_zone.zone as dropoff_zone,
    fhv_data.pickup_datetime,
    fhv_data.dropoff_datetime,
    fhv_data.sr_flag,
    fhv_data.affiliated_base_num
from fhv_data
inner join dim_zones as zoned_pickup_zone
on fhv_data.pickup_locationid = zoned_pickup_zone.locationid
inner join dim_zones as zones_dropoff_zone
on fhv_data.dropoff_locationid = zones_dropoff_zone.locationid