# Module 1 Homework: Docker & SQL

## Question 1. Understanding Docker images

Run docker with the `python:3.13` image. Use an entrypoint `bash` to interact with the container.

What's the version of `pip` in the image?

- 25.3
- 24.3.1
- 24.2.1
- 23.3.1

## Answer Question1
Answer - 25.3

---

## Question 2. Understanding Docker networking and docker-compose

Given the following `docker-compose.yaml`, what is the `hostname` and `port` that pgadmin should use to connect to the postgres database?

```yaml
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

- postgres:5433
- localhost:5432
- db:5433
- postgres:5432
- db:5432

## Answer Question2
Answer - db:5432  
If multiple answers are correct, select any.

---

## Question 3. Counting short trips

For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a `trip_distance` of less than or equal to 1 mile?

- 7,853
- 8,007
- 8,254
- 8,421

## Answer Question3
```sql
-- SQL Query:
SELECT COUNT(*) AS trips_le_1_mile
FROM green_taxi_trips
WHERE lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance <= 1;
```

Answer - 8007

---

## Question 4. Longest trip for each day

Which was the pick up day with the longest trip distance? Only consider trips with `trip_distance` less than 100 miles (to exclude data errors).

Use the pick up time for your calculations.

- 2025-11-14
- 2025-11-20
- 2025-11-23
- 2025-11-25

## Answer Question4
```sql
-- SQL Query:
SELECT
  DATE(lpep_pickup_datetime) AS pick_up_day,
  trip_distance AS long_trip_distance
FROM green_taxi_trips
WHERE trip_distance < 100
ORDER BY trip_distance DESC
LIMIT 1;
```

Answer - 2025-11-14

---

## Question 5. Biggest pickup zone

Which was the pickup zone with the largest `total_amount` (sum of all trips) on November 18th, 2025?

- East Harlem North
- East Harlem South
- Morningside Heights
- Forest Hills

## Answer Question5
```sql
-- SQL Query:
SELECT
  tzl."Zone",
  SUM(gtt.total_amount) AS total_revenue
FROM green_taxi_trips gtt
JOIN taxi_zone_lookup tzl
  ON gtt."PULocationID" = tzl."LocationID"
WHERE DATE(gtt.lpep_pickup_datetime) = '2025-11-18'
GROUP BY tzl."Zone"
ORDER BY total_revenue DESC
LIMIT 1;
```

Answer - East Harlem North

---

## Question 6. Largest tip

For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

Note: it's `tip` , not `trip`. We need the name of the zone, not the ID.

- JFK Airport
- Yorkville West
- East Harlem North
- LaGuardia Airport

## Answer Question6
```sql
-- SQL Query:
SELECT dz."Zone" AS dropoff_zone,
       MAX(gtt.tip_amount) AS max_tip
FROM green_taxi_trips gtt
JOIN taxi_zone_lookup pz
  ON gtt."PULocationID" = pz."LocationID"
JOIN taxi_zone_lookup dz
  ON gtt."DOLocationID" = dz."LocationID"
WHERE pz."Zone" = 'East Harlem North'
  AND gtt.lpep_pickup_datetime >= DATE '2025-11-01'
  AND gtt.lpep_pickup_datetime <  DATE '2025-12-01'
GROUP BY dz."Zone"
ORDER BY max_tip DESC
LIMIT 1;
```

Answer - Yorkville West

---

## Terraform

## Question 7. Terraform Workflow

Which of the following sequences, respectively, describes the workflow for:  
1. Downloading the provider plugins and setting up backend,  
2. Generating proposed changes and auto-executing the plan  
3. Remove all resources managed by Terraform

Answers:

- terraform import, terraform apply -y, terraform destroy  
- terraform init, terraform plan -auto-apply, terraform rm  
- terraform init, terraform run -auto-approve, terraform destroy  
- terraform init, terraform apply -auto-approve, terraform destroy  
- terraform import, terraform apply -y, terraform rm

## Answer Question7
Answer - terraform init, terraform apply -auto-approve, terraform destroy  

Explanation:

- `terraform init`  
  It initializes the Terraform working directory. It downloads provider plugins and configures the backend.

- `terraform apply -auto-approve`  
  It creates an execution plan and automatically applies the changes without asking for confirmation.

- `terraform destroy`  
  It removes all resources managed by Terraform and cleans up the infrastructure completely.

