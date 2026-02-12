import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:postgres@localhost:5433/ny_taxi')

'''Question 3: Counting short trips'''

query_q3 = """
SELECT COUNT(*) AS trips_le_1_mile 
FROM green_taxi_trips
WHERE lpep_pickup_datetime >= '2025-11-01' 
  AND lpep_pickup_datetime < '2025-12-01'
	AND trip_distance <=1;"""

'''Question 4: Longest trip for each day'''

query_q4 ="""
SELECT
  DATE(lpep_pickup_datetime) AS pick_up_day,
  trip_distance AS long_trip_distance
FROM green_taxi_trips
WHERE trip_distance < 100
ORDER BY trip_distance DESC
LIMIT 1;"""


'''Question 5. Biggest pickup zone"'''

query_q5 = """
SELECT
  tzl."Zone",
  SUM(gtt.total_amount) AS total_revenue
FROM green_taxi_trips gtt
JOIN taxi_zone_lookup tzl
  ON gtt."PULocationID" = tzl."LocationID"
WHERE DATE(gtt.lpep_pickup_datetime) = '2025-11-18'
GROUP BY tzl."Zone"
ORDER BY SUM(gtt.total_amount) DESC
LIMIT 1;
"""

'''Question 6. Largest tip'''

query_q6 = """
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
"""

print("Question 3. Counting short trips")
print(pd.read_sql(query_q3, engine))
print("Question 4. Longest trip for each day")
print(pd.read_sql(query_q4, engine))
print("Question 5. Biggest pickup zone")
print(pd.read_sql(query_q5, engine))
print("Question 6. Largest tip")
print(pd.read_sql(query_q6, engine))