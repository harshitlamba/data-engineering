import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click

def run(prefix, year, month, dtype, parse_dates, chunksize, engine, pg_table):
    # load the data chunk-wise to postgres database
    first = True
    df_iter = pd.read_csv(prefix + f'yellow_tripdata_{year}-{month:02d}.csv.gz', 
                        dtype=dtype, parse_dates=parse_dates, iterator=True, chunksize=chunksize)

    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(0).to_sql(name=pg_table, con=engine, if_exists='replace')
            first = False
            print('Table Created.')
        df_chunk.to_sql(name=pg_table, con=engine, if_exists='append')

        print("Inserted:", len(df_chunk))

@click.command()
@click.option('--host', default='localhost', help='PostgreSQL host')
@click.option('--port', default=5432, help='PostgreSQL port')
@click.option('--user', default='root', help='PostgreSQL user')
@click.option('--password', default='root', help='PostgreSQL password')
@click.option('--db', default='ny-taxi-db', help='PostgreSQL database name')
@click.option('--table', default=None, help='PostgreSQL table name')
@click.option('--year', default=2021, type=int, help='Year of the data')
@click.option('--month', default=1, type=int, help='Month of the data')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for ingestion')

def main(host, port, user, password, db, table, year, month, chunksize):    
    '''Ingest NYC taxi dataset into PostgreSQL database'''
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'

    if table is None:
        table = f'yellow_taxi_trips_{year}_{month:02d}'

    # explicitly state the column datatypes as pandas might read them differently
    dtype = {
        "VendorID": "Int64",
        "passenger_count": "Int64",
        "trip_distance": "float64",
        "RatecodeID": "Int64",
        "store_and_fwd_flag": "string",
        "PULocationID": "Int64",
        "DOLocationID": "Int64",
        "payment_type": "Int64",
        "fare_amount": "float64",
        "extra": "float64",
        "mta_tax": "float64",
        "tip_amount": "float64",
        "tolls_amount": "float64",
        "improvement_surcharge": "float64",
        "total_amount": "float64",
        "congestion_surcharge": "float64"
    }

    parse_dates = [
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime"
    ]

    # set up the postgres engine
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # call run() that will insert the data in postgres
    run(prefix, year, month, dtype, parse_dates, chunksize, engine, table)

    print("Insert Completed.")

if __name__=='__main__':
    main()


