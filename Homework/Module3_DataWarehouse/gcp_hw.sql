CREATE OR REPLACE EXTERNAL TABLE `zoomcamp-mod3-datawarehouse.nytaxi.external_yellow_tripdata`
OPTIONS (
  format = 'parquet',
  uris = ['gs://zoomcamp_hw3_2025/yellow_tripdata_2024-*.parquet']
);

CREATE OR REPLACE TABLE `zoomcamp-mod3-datawarehouse.nytaxi.external_yellow_nonpartitioned_tripdata`
AS SELECT * FROM `zoomcamp-mod3-datawarehouse.nytaxi.external_yellow_tripdata`;

SELECT count(*) FROM `zoomcamp-mod3-datawarehouse.nytaxi.external_yellow_tripdata`
-- 20332093
SELECT count(distinct PULocationID) FROM `zoomcamp-mod3-datawarehouse.nytaxi.external_yellow_nonpartitioned_tripdata` --external_yellow_tripdata
-- 0 MB for the External Table and 155.12 MB for the Materialized Table

SELECT PULocationID FROM `zoomcamp-mod3-datawarehouse.nytaxi.external_yellow_nonpartitioned_tripdata`;
--155.12MB
SELECT PULocationID,DOLocationID FROM `zoomcamp-mod3-datawarehouse.nytaxi.external_yellow_nonpartitioned_tripdata`;
--310.24MB

select count(1) from `nytaxi.external_yellow_tripdata` where fare_amount=0
--8333

CREATE OR REPLACE TABLE `zoomcamp-mod3-datawarehouse.nytaxi.yellow_tripdata_partitioned_clustered`
PARTITION BY
  DATE(tpep_dropoff_datetime)
CLUSTER BY 
  VendorID AS
SELECT * FROM `zoomcamp-mod3-datawarehouse.nytaxi.external_yellow_tripdata`

select distinct VendorID 
from `zoomcamp-mod3-datawarehouse.nytaxi.external_yellow_nonpartitioned_tripdata`
where DATE(tpep_dropoff_datetime) between '2024-03-01' and '2024-03-16'
--310.24MB

select distinct VendorID 
from `zoomcamp-mod3-datawarehouse.nytaxi.yellow_tripdata_partitioned_clustered`
where DATE(tpep_dropoff_datetime) between '2024-03-01' and '2024-03-16'
--28.84MB