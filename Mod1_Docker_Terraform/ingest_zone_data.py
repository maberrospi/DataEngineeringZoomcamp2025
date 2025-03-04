import os
import argparse

from time import time

import pandas as pd
from sqlalchemy import create_engine

def main(params) -> None: 
    
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    url = params.url
    
    if url.endswith('.csv.gz'):
        csv_name = 'taxi_zone_lookup.csv.gz'
    else:
        csv_name = 'taxi_zone_lookup.csv'

    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    # engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
    # engine.connect()

    df_zones = pd.read_csv("taxi_zone_lookup.csv")
    df_zones.to_sql(name='zones', con=engine, if_exists='replace')
    
    print("All done!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--url', required=True, help='url of the csv file')

    args = parser.parse_args()

    main(args)

