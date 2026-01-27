import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine
import click
from tqdm.auto import tqdm

def run(engine, table, filepath, filename, chunksize):
    df_iter = None
    filetype = filename.rsplit('.',1)[1]
    match filetype:
        case 'csv':
            df_iter = pd.read_csv(filepath + filename, chunksize=chunksize, iterator=True)
            first = True
            for df_chunk in tqdm(df_iter):
                if first:
                    df_chunk.head(0).to_sql(name=table, con=engine, if_exists='replace', index=False)
                    first = False
                    print('Table Created.')
                df_chunk.to_sql(name=table, con=engine, if_exists='append', index=False)
                print("Inserted:", len(df_chunk))
        case 'parquet':
            parquet_file = pq.ParquetFile(filepath + filename)
            first = True
            for df_chunk in tqdm(parquet_file.iter_batches(batch_size=chunksize)):
                df = df_chunk.to_pandas()
                if first:
                    df.head(0).to_sql(name=table, con=engine, if_exists='replace', index=False)
                    first = False
                    print('Table Created.')
                df.to_sql(name=table, con=engine, if_exists='append', index=False, method='multi')
                print("Inserted:", len(df))
        case _:
            df_iter = None

    if df_iter is None:        
        print('Please enter a valid filetype argument. Available options: csv or parquet.')

@click.command()
@click.option('--host', default='localhost', help='PostgreSQL host')
@click.option('--port', default=5432, help='PostgreSQL port')
@click.option('--user', default='root', help='PostgreSQL user')
@click.option('--password', default='root', help='PostgreSQL password')
@click.option('--db', default='module-one-db', help='PostgreSQL database name')
@click.option('--table', required=True, help='PostgreSQL table name')
@click.option('--filepath', required=True, default='./', help='Data file path')
@click.option('--filename', required=True, help='Data filename')
@click.option('--chunksize', required=True, default=100000, type=int, help='Chunk size for ingestion')

def main(host, port, user, password, db, table, filepath, filename, chunksize):
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    run(engine, table, filepath, filename, chunksize)
    print('Insert complete.')

if __name__=='__main__':
    main()

