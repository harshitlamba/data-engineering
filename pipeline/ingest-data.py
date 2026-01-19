import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

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

def main():    
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    year = 2021
    month = 1
    chunksize = 100000

    pg_host = 'localhost'
    pg_port = 5432
    pg_user = 'root'
    pg_password = 'root'
    pg_db = 'ny-taxi-db'
    pg_table = 'yellow_taxi_data'

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
    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}')

    # call run() that will insert the data in postgres
    run(prefix, year, month, dtype, parse_dates, chunksize, engine, pg_table)

    print("Insert Completed.")

if __name__=='__main__':
    main()


