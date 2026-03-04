from google.cloud import bigquery
client = bigquery.Client()

query_q3 = """
                SELECT 
                    COUNT(*) as total_records 
              
                FROM `de-zoomcamp-486100.dbt_nyctaxi_prod.fct_monthly_zone_revenue`"""

query_q4 = """  SELECT 
                    pickup_zone,
                    SUM(revenue_monthly_total_amount) as total_revenue
               FROM `de-zoomcamp-486100.dbt_nyctaxi_prod.fct_monthly_zone_revenue`
               WHERE service_type = 'Green'
               AND EXTRACT(YEAR FROM revenue_month) = 2020
               GROUP BY pickup_zone
               ORDER BY total_revenue DESC
               LIMIT 1;"""
query_q5 = """
              SELECT
                    SUM(total_monthly_trips) as total_trips
              FROM `de-zoomcamp-486100.dbt_nyctaxi_prod.fct_monthly_zone_revenue`
              WHERE service_type = 'Green'
              AND revenue_month >= '2019-10-01'
              AND revenue_month < '2019-11-01';"""

query_q6 = """
           SELECT 
               COUNT(*) as total_fhv_records 
           FROM `de-zoomcamp-486100.dbt_nyctaxi_prod.stg_fhv_tripdata`;
           """ 

df1= client.query(query_q3).to_dataframe()
df2= client.query(query_q4).to_dataframe()
df3= client.query(query_q5).to_dataframe()
df4= client.query(query_q6).to_dataframe()

print("Question 3. Counting Records in fct_monthly_zone_revenue")
print(df1)
print("Question 4. Best Performing Zone for Green Taxis (2020)")
print(df2)
print("Question 5. Green Taxi Trip Counts (October 2019)")
print(df3)
print("Question 6. Build a Staging Model for FHV Data")
print(df4)
