CREATE TABLE `zoomcamp-mod4-analyticseng.trips_data_all.green_tripdata` AS
SELECT * FROM `bigquery-public-data.new_york_taxi_trips.tlc_green_trips_2019`;

CREATE TABLE `zoomcamp-mod4-analyticseng.trips_data_all.yellow_tripdata` AS
SELECT * FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2019`;

insert into `zoomcamp-mod4-analyticseng.trips_data_all.green_tripdata`
SELECT * FROM `bigquery-public-data.new_york_taxi_trips.tlc_green_trips_2020`;

insert into `zoomcamp-mod4-analyticseng.trips_data_all.yellow_tripdata`
SELECT * FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2020`;

-- Check everything is okay
select * from `zoomcamp-mod4-analyticseng.trips_data_all.green_tripdata` where EXTRACT(year from DATE(pickup_datetime))=2019 limit 100


  -- Fixes green table schema
ALTER TABLE `zoomcamp-mod4-analyticseng.trips_data_all.green_tripdata`
  RENAME COLUMN vendor_id TO VendorID;
ALTER TABLE `zoomcamp-mod4-analyticseng.trips_data_all.green_tripdata`
  RENAME COLUMN pickup_datetime TO lpep_pickup_datetime;
ALTER TABLE `zoomcamp-mod4-analyticseng.trips_data_all.green_tripdata`
  RENAME COLUMN dropoff_datetime TO lpep_dropoff_datetime;
ALTER TABLE `zoomcamp-mod4-analyticseng.trips_data_all.green_tripdata`
  RENAME COLUMN rate_code TO RatecodeID;
ALTER TABLE `zoomcamp-mod4-analyticseng.trips_data_all.green_tripdata`
  RENAME COLUMN imp_surcharge TO improvement_surcharge;
ALTER TABLE `zoomcamp-mod4-analyticseng.trips_data_all.green_tripdata`
  RENAME COLUMN pickup_location_id TO PULocationID;
ALTER TABLE `zoomcamp-mod4-analyticseng.trips_data_all.green_tripdata`
  RENAME COLUMN dropoff_location_id TO DOLocationID;

  -- Fixes yellow table schema
ALTER TABLE `zoomcamp-mod4-analyticseng.trips_data_all.yellow_tripdata`
  RENAME COLUMN vendor_id TO VendorID;
ALTER TABLE `zoomcamp-mod4-analyticseng.trips_data_all.yellow_tripdata`
  RENAME COLUMN pickup_datetime TO tpep_pickup_datetime;
ALTER TABLE `zoomcamp-mod4-analyticseng.trips_data_all.yellow_tripdata`
  RENAME COLUMN dropoff_datetime TO tpep_dropoff_datetime;
ALTER TABLE `zoomcamp-mod4-analyticseng.trips_data_all.yellow_tripdata`
  RENAME COLUMN rate_code TO RatecodeID;
ALTER TABLE `zoomcamp-mod4-analyticseng.trips_data_all.yellow_tripdata`
  RENAME COLUMN imp_surcharge TO improvement_surcharge;
ALTER TABLE `zoomcamp-mod4-analyticseng.trips_data_all.yellow_tripdata`
  RENAME COLUMN pickup_location_id TO PULocationID;
ALTER TABLE `zoomcamp-mod4-analyticseng.trips_data_all.yellow_tripdata`
  RENAME COLUMN dropoff_location_id TO DOLocationID;