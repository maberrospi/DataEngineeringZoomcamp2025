CREATE OR REPLACE EXTERNAL TABLE `zoomcamp-mod4-analyticseng.trips_data_all.external_fhv_data_norm` 
OPTIONS (
  format='parquet',
  uris = ['gs://zoomcamp_hw4_2025_norm/fhv_tripdata_2019-*.parquet']
);

-- Check everything works alright
select * from `zoomcamp-mod4-analyticseng.trips_data_all.external_fhv_data_norm` limit 10;

-- Create table from external table
CREATE OR REPLACE TABLE `zoomcamp-mod4-analyticseng.trips_data_all.fhv_tripdata` AS
SELECT * FROM `zoomcamp-mod4-analyticseng.trips_data_all.external_fhv_data_norm`;