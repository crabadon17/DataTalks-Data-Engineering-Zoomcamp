
import click
import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine
from tqdm.auto import tqdm


@click.command()
@click.option('--pg-user', default='root')
@click.option('--pg-pass', default='root')
@click.option('--pg-host', default='localhost')
@click.option('--pg-port', default=5432, type=int)
@click.option('--pg-db', default='ny_taxi')
@click.option('--trip-table', default='green_taxi_trips')
@click.option('--zone-table', default='taxi_zone_lookup')
@click.option('--chunksize', default=100000, type=int)
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, trip_table, zone_table, chunksize):

    engine = create_engine(
        f'postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'
    )

    
    taxi_zone = pd.read_csv("taxi_zone_lookup.csv")

    taxi_zone.to_sql(
        name=zone_table,
        con=engine,
        if_exists="replace",
        index=False
    )

    print("Zone lookup loaded")

    green_taxi_trips = pq.ParquetFile("green_tripdata_2025-11.parquet")

    first = True

    for batch in tqdm(green_taxi_trips.iter_batches(batch_size=chunksize)):
        df_chunk = batch.to_pandas()

        if first:
            df_chunk.head(0).to_sql(
                name=trip_table,
                con=engine,
                if_exists="replace",
                index=False
            )
            first = False

        df_chunk.to_sql(
            name=trip_table,
            con=engine,
            if_exists="append",
            index=False
        )

    print("Green taxi trips loaded")


if __name__ == "__main__":
    run()