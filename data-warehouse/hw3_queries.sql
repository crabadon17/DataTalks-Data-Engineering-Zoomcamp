--Query for creating external table
CREATE OR REPLACE EXTERNAL TABLE `de-zoomcamp-486100.nytaxi.external_yellow_tripdata_2024`
OPTIONS (
  format = 'PARQUET',
  uris = [
    'gs://dwh_hw3_2026/yellow_tripdata_2024-*.parquet',
  ],
);

--Query for creating materialized or regular table
CREATE OR REPLACE  `de-zoomcamp-486100.nytaxi.materialized_yellow_tripdata_2024` AS
SELECT * FROM `de-zoomcamp-486100.nytaxi.external_yellow_tripdata_2024`

--Query for Question 1:Counting Records 
--Answer: 20,332,093
SELECT COUNT(*) FROM `de-zoomcamp-486100.nytaxi.materialized_yellow_tripdata_2024` 

--Query for Question 2: Data read estimation
-- Answer:0 MB for the External Table and 155.12 MB for the Materialized Table

--Query to count the distinct number of PULocationIDs for the entire dataset on external table.
-- Estimation Bytes in eternal table: 0 MB 
SELECT COUNT(DISTINCT PULocationID) FROM `de-zoomcamp-486100.nytaxi.external_yellow_tripdata_2024`

--Query to count the distinct number of PULocationIDs for the entire dataset on regular table.
-- Estimation Bytes in regular table: 155.12 MB 
SELECT COUNT(DISTINCT PULocationID) FROM `de-zoomcamp-486100.nytaxi.materialized_yellow_tripdata_2024`

--Query for Question3: Understanding columnar storage
-- Estimation Bytes: 155.12 MB 
SELECT  PULocationID FROM `de-zoomcamp-486100.nytaxi.materialized_yellow_tripdata_2024`;
-- Estimation Bytes: 310.24 MB 
SELECT  PULocationID,DOLocationID FROM `de-zoomcamp-486100.nytaxi.materialized_yellow_tripdata_2024`

--Query for Question4: Counting zero fare trips
--Answer:8,333

SELECT COUNT(*) AS zero_fare_trips FROM `de-zoomcamp-486100.nytaxi.materialized_yellow_tripdata_2024` 
WHERE fare_amount = 0;

--Query for Question5:Partitioning and clustering
--Answer:Partition by tpep_dropoff_datetime and Cluster on VendorID

CREATE OR REPLACE TABLE `de-zoomcamp-486100.nytaxi.yellow_tripdata_partitioned_clustered_2024`
PARTITION BY DATE(tpep_pickup_datetime)
CLUSTER BY VendorID AS
SELECT *
FROM `de-zoomcamp-486100.nytaxi.external_yellow_tripdata_2024`;

--Query for Question6:Partition benefits
--Answer:310.24 MB for non-partitioned table and 26.84 MB for the partitioned table

--Estimation Bytes in non-partitioned table:310.24 MB 
SELECT DISTINCT VendorID
FROM `de-zoomcamp-486100.nytaxi.materialized_yellow_tripdata_2024`
WHERE tpep_dropoff_datetime BETWEEN "2024-03-01" AND "2024-03-15";
--Estimation Bytes in partitioned table:26.86 MB
SELECT DISTINCT VendorID
FROM `de-zoomcamp-486100.nytaxi.yellow_tripdata_partitioned_clustered_2024`
WHERE tpep_dropoff_datetime BETWEEN "2024-03-01" AND "2024-03-15"

--Query for Question9:Understanding table scans
--Estimation Bytes : 0 B
SELECT COUNT(*)
FROM `de-zoomcamp-486100.nytaxi.materialized_yellow_tripdata_2024`
