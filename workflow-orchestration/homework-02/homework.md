# Kestra + BigQuery Taxi Data – Workflow Homework Answer
## 1. Project Overview

This document explains how the **Kestra workflow** for taxi data was executed, validated, and analyzed.

**Key Components:**

* **Kestra flows** with schedule triggers and backfills
* **CSV ingestion** into BigQuery
* **SQL validation queries** for row counts and file properties
* **Local execution** using Docker Compose with PostgreSQL as metadata backend

**Services Setup:**

```bash
docker-compose up -d
```

* **Kestra UI:** [http://localhost:8080](http://localhost:8080)
* **PgAdmin:** [http://localhost:8085](http://localhost:8085)

---

## 2. Workflow Design

The `taxi_flow` automates data processing for Yellow and Green taxi datasets:

1. **Triggering**

   * Monthly schedule triggers for Yellow and Green taxis
   * Backfills for historical data

2. **Extraction**

   * Downloads CSV for the specified month and taxi type

3. **Validation**

   * Logs **uncompressed file size**

4. **Storage**

   * Uploads raw CSV to **Google Cloud Storage**
   * Creates external tables in **BigQuery**

5. **Loading**

   * Loads data into **partitioned BigQuery tables**
   * Merges rows using deterministic `unique_row_id`

6. **Cleanup**

   * Deletes local CSVs after successful ingestion

---

## 3. File Processing Observations

### 3.1 Yellow Taxi – December 2020

* CSV: `yellow_tripdata_2020-12.csv`
* Uncompressed size observed in Buckets in Google Cloud Storage: **134.5 MiB**

### 3.2 Green Taxi – April 2020

* Filename template: `{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv`
* Rendered filename: `green_tripdata_2020-04.csv`

---

## 4. Row Count Validation in BigQuery

### 4.1 Yellow Taxi – Year 2020

```sql
SELECT COUNT(*)
FROM `project.dataset.yellow_tripdata`
WHERE EXTRACT(YEAR FROM tpep_pickup_datetime) = 2020;
```

* Result: **24,648,499 rows**

### 4.2 Green Taxi – Year 2020

```sql
SELECT COUNT(*)
FROM `project.dataset.green_tripdata`
WHERE EXTRACT(YEAR FROM lpep_pickup_datetime) = 2020;
```

* Result: **1,734,051 rows**

### 4.3 Yellow Taxi – March 2021

```sql
SELECT COUNT(*)
FROM `project.dataset.yellow_tripdata`
WHERE EXTRACT(YEAR FROM tpep_pickup_datetime) = 2021
  AND EXTRACT(MONTH FROM tpep_pickup_datetime) = 3;
```

* Result: **1,925,152 rows**

---

## 5. Schedule Trigger Configuration

To run workflows with New York timezone:

```yaml
schedule:
  cron: "0 0 1 * *"  # first day of each month
  timezone: "America/New_York"
```

**Notes:**

* Ensures all triggers respect daylight saving changes
* Best practice: use IANA timezone format

---

## 6. Key Lessons

1. **Dynamic file rendering**: Input variables make workflow reusable for multiple taxi types and months.
2. **Backfills**: Efficient way to process historical data without manual re-execution.
3. **BigQuery as source of truth**: Reliable for verifying row counts and validating ingestion.
4. **Cleanup**: Removing local CSVs prevents storage bloat and ensures reproducibility.
