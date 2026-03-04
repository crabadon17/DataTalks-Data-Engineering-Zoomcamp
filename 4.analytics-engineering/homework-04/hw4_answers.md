# Module 4 Homework: Analytics Engineering with dbt

In this homework, we'll use the dbt project in `04-analytics-engineering/taxi_rides_ny/` to transform NYC taxi data and answer questions by querying the models.

## Setup

1. Set up your dbt project following the [setup guide](../../../04-analytics-engineering/setup/)
2. Load the Green and Yellow taxi data for 2019-2020 and FHV trip data for 2019 into your warehouse (use static tables from [dtc github](https://github.com/DataTalksClub/nyc-tlc-data/), don't use offical tables from tlc because some values change from time to time)
3. Run `dbt build --target prod` to create all models and run tests

> **Note:** By default, dbt uses the `dev` target. You must use `--target prod` to build the models in the production dataset, which is required for the homework queries below.

After a successful build, you should have models like `fct_trips`, `dim_zones`, and `fct_monthly_zone_revenue` in your warehouse.

---

### Question 1. dbt Lineage and Execution

Given a dbt project with the following structure:

```
models/
├── staging/
│   ├── stg_green_tripdata.sql
│   └── stg_yellow_tripdata.sql
└── intermediate/
    └── int_trips_unioned.sql (depends on stg_green_tripdata & stg_yellow_tripdata)
```

If you run `dbt run --select int_trips_unioned`, what models will be built?

- `stg_green_tripdata`, `stg_yellow_tripdata`, and `int_trips_unioned` (upstream dependencies)
- Any model with upstream and downstream dependencies to `int_trips_unioned`
- `int_trips_unioned` only
- `int_trips_unioned`, `int_trips`, and `fct_trips` (downstream dependencies)

Answer:`int_trips_unioned` only
Explanation:dbt run --select runs just the model you name, ignoring other related models.
---

### Question 2. dbt Tests

You've configured a generic test like this in your `schema.yml`:

```yaml
columns:
  - name: payment_type
    data_tests:
      - accepted_values:
          arguments:
            values: [1, 2, 3, 4, 5]
            quote: false
```

Your model `fct_trips` has been running successfully for months. A new value `6` now appears in the source data.

What happens when you run `dbt test --select fct_trips`?

- dbt will skip the test because the model didn't change
- dbt will fail the test, returning a non-zero exit code
- dbt will pass the test with a warning about the new value
- dbt will update the configuration to include the new value
Answer: dbt will fail the test, returning a non-zero exit code
Explanation: dbt test checks the data, not the model. The new value 6 violates an accepted_values test, so the test fails and returns a non-zero exit code.
---

### Question 3. Counting Records in `fct_monthly_zone_revenue`

After running your dbt project, query the `fct_monthly_zone_revenue` model.

What is the count of records in the `fct_monthly_zone_revenue` model?

- 12,998
- 14,120
- 12,184
- 15,421
Answer:12,184
Sql used in Bigquery
```sql
  SELECT 
        COUNT(*) as total_records 
  FROM `de-zoomcamp-486100.dbt_nyctaxi_prod.fct_monthly_zone_revenue`
```
---

### Question 4. Best Performing Zone for Green Taxis (2020)

Using the `fct_monthly_zone_revenue` table, find the pickup zone with the **highest total revenue** (`revenue_monthly_total_amount`) for **Green** taxi trips in 2020.

Which zone had the highest revenue?

- East Harlem North
- Morningside Heights
- East Harlem South
- Washington Heights South
Answer:East Harlem North the highest total revenue of 1817469.05
Sql used in Bigquery
```sql
    SELECT 
          pickup_zone,
          SUM(revenue_monthly_total_amount) as total_revenue
    FROM `de-zoomcamp-486100.dbt_nyctaxi_prod.fct_monthly_zone_revenue`
    WHERE service_type = 'Green'
    AND EXTRACT(YEAR FROM revenue_month) = 2020
    GROUP BY pickup_zone
    ORDER BY total_revenue DESC
    LIMIT 1;"""
   
```
---

### Question 5. Green Taxi Trip Counts (October 2019)

Using the `fct_monthly_zone_revenue` table, what is the **total number of trips** (`total_monthly_trips`) for Green taxis in October 2019?

- 500,234
- 350,891
- 384,624
- 421,509

Answer:384,624
Sql used in Bigquery
```sql
   SELECT
        SUM(total_monthly_trips) as total_trips
   FROM `de-zoomcamp-486100.dbt_nyctaxi_prod.fct_monthly_zone_revenue`
   WHERE service_type = 'Green'
   AND revenue_month >= '2019-10-01'
   AND revenue_month < '2019-11-01';"""
```
---

### Question 6. Build a Staging Model for FHV Data

Create a staging model for the **For-Hire Vehicle (FHV)** trip data for 2019.

1. Load the [FHV trip data for 2019](https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/fhv) into your data warehouse
2. Create a staging model `stg_fhv_tripdata` with these requirements:
   - Filter out records where `dispatching_base_num IS NULL`
   - Rename fields to match your project's naming conventions (e.g., `PUlocationID` → `pickup_location_id`)

What is the count of records in `stg_fhv_tripdata`?

- 42,084,899
- 43,244,693
- 22,998,722
- 44,112,187

Solution:
Step 1: Load data in datawarehouse for this homework activity I used Google Cloud Storage. 
```python gcs_fhv.py"
```
Step 2: Create a staging model base of the given requirements.
```sql
  select
    dispatching_base_num,
    cast(pickup_datetime as timestamp) as pickup_datetime,
    cast(dropoff_datetime as timestamp) as dropoff_datetime,
    cast(pulocationid as integer) as pickup_location_id,
    cast(dolocationid as integer) as dropoff_location_id,
    sr_flag,
    affiliated_base_number
  from {{ source('raw', 'fhv_tripdata') }}
  where dispatching_base_num is not null 
  and dispatching_base_num != ''
```
Step 3: Add new sources for fhv_tripdata
```yml
  - name: fhv_tripdata
        description: Raw for-hire vehicle (FHV) trip records for 2019
        columns:
          - name: dispatching_base_num
            description: Base number for the dispatching company
```
Step 4: Count the records of stg_fhv_tripdata
SQL used in Bigquery
```sql
    SELECT 
       COUNT(*) as total_fhv_records 
    FROM `de-zoomcamp-486100.dbt_nyctaxi_prod.stg_fhv_tripdata`
```
Answer:43,244,693 was the total records of stg_fhv_tripdata only 3 nulls left out base on original data in fhv_tripdata in the total of 43,244,696.
---


