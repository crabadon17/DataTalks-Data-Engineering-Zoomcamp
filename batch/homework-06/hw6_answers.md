# Module 6 Homework

In this homework we'll put what we learned about Spark in practice.

For this homework we will be using the Yellow 2025-11 data from the official website:

```bash
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-11.parquet
```


## Question 1: Install Spark and PySpark

- Install Spark
- Run PySpark
- Create a local spark session
- Execute spark.version.

What's the output?
Answer : The sparks.version print the version of Spark included with PySpark, I used windows setup for installation in my case the output was 4.1.1.

> [!NOTE]
> To install PySpark follow this [guide](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/06-batch/setup/)


## Question 2: Yellow November 2025

Read the November 2025 Yellow into a Spark Dataframe.

Repartition the Dataframe to 4 partitions and save it to parquet.

What is the average size of the Parquet (ending with .parquet extension) Files that were created (in MB)? Select the answer which most closely matches.

- 6MB
- 25MB
- 75MB
- 100MB

Answer : The average size of the parquet that get downloaded was 25MB.


## Question 3: Count records

How many taxi trips were there on the 15th of November?

Consider only trips that started on the 15th of November.

- 62,610
- 102,340
- 162,604
- 225,768

```python
  spark.sql("""
    SELECT COUNT(*) AS total_trips 
    FROM yellow_nov_data
    WHERE pickup_date = '2025-11-15'
""").show()
```
Answer: Using Spark SQL, the total number of trips in the data on November 15 was 162,604.

## Question 4: Longest trip

What is the length of the longest trip in the dataset in hours?

- 22.7
- 58.2
- 90.6
- 134.5

```python
  spark.sql("""
  SELECT ROUND(MAX((unix_timestamp(tpep_dropoff_datetime) - unix_timestamp(tpep_pickup_datetime)) / 3600), 1) 
  AS longest_trip_hour
  FROM yellow_nov_data
  """).show()
```
Answer: Using Spark SQL, the longest trip was 90.6 hours. Unlike traditional SQL databases that can directly handle time arithmetic, PySpark often uses the unix_timestamp() function to convert timestamps into numeric values for easier aggregation and duration calculations.

## Question 5: User Interface

Spark's User Interface which shows the application's dashboard runs on which local port?

- 80
- 443
- 4040
- 8080
Answer: Port 4040 is used to open the Spark UI, which shows the dashboard of a running Spark application. 



## Question 6: Least frequent pickup location zone

Load the zone lookup data into a temp view in Spark:

```bash
wget https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
```

Using the zone lookup data and the Yellow November 2025 data, what is the name of the LEAST frequent pickup location Zone?

- Governor's Island/Ellis Island/Liberty Island
- Arden Heights
- Rikers Island
- Jamaica Bay

If multiple answers are correct, select any

```python
  spark.sql("""
  WITH zone_counts AS (
      SELECT t.Zone, COUNT(*) AS trip_count
      FROM yellow_nov_data y
      JOIN taxi_zone_lookup t
        ON y.PULocationID = t.LocationID
      GROUP BY t.Zone
  )
  SELECT Zone, trip_count
  FROM zone_counts
  WHERE trip_count = (SELECT MIN(trip_count) FROM zone_counts)
  """).show()

```
Answer:Using Spark SQL, the pickup zones with only 1 trip were Governor's Island/Ellis Island/Liberty Island and Arden Heights. Eltingville/Annadale/Prince's Bay was not included in the answer choices.
