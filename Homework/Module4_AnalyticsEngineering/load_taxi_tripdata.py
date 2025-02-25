import os
import sys
import urllib.request
import requests
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import argparse
from pathlib import Path
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor
from google.cloud import storage
from google.api_core.exceptions import NotFound, Forbidden
import time


# Change this to your bucket name
BUCKET_NAME = "zoomcamp2025_hw4_green_norm"

# If you authenticated through the GCP SDK you can comment out these two lines
# CREDENTIALS_FILE = "gcs.json"
client = storage.Client(project="zoomcamp-mod4-analyticseng")


# BASE_URL_PARQUET = "https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_2019-"
BASE_URL_PARQUET = "https://d37ci6vzurychx.cloudfront.net/trip-data/"
BASE_URL_CSV = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/"
# https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-01.csv.gz
MONTHS = [f"{i:02d}" for i in range(1, 13)]
DOWNLOAD_DIR = "."

CHUNK_SIZE = 8 * 1024 * 1024

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

bucket = client.bucket(BUCKET_NAME)

fhv_schema = pa.schema([
        pa.field('dispatching_base_num',pa.string()),
        pa.field("pickup_datetime",pa.timestamp('s')),
        pa.field("dropOff_datetime",pa.timestamp('s')),
        pa.field("PUlocationID",pa.int64()),
        pa.field("DOlocationID",pa.int64()),
        pa.field("SR_Flag",pa.int64()),
        pa.field("Affiliated_base_number",pa.string())
    ])


yellow_schema = pa.schema([
    ("VendorID", pa.string()),
    ("tpep_pickup_datetime", pa.timestamp("s")),
    ("tpep_dropoff_datetime", pa.timestamp("s")),
    ("passenger_count", pa.int32()),
    ("trip_distance", pa.decimal128(38, 9)),
    ("RatecodeID", pa.string()),
    ("store_and_fwd_flag", pa.string()),
    ("PULocationID", pa.string()),
    ("DOLocationID", pa.string()),
    ("payment_type", pa.int32()),
    ("fare_amount", pa.decimal128(38, 9)),
    ("extra", pa.decimal128(38, 9)),
    ("mta_tax", pa.decimal128(38, 9)),
    ("tip_amount", pa.decimal128(38, 9)),
    ("tolls_amount", pa.decimal128(38, 9)),
    ("improvement_surcharge", pa.decimal128(38, 9)),
    ("total_amount", pa.decimal128(38, 9)),
    ("congestion_surcharge", pa.decimal128(38, 9)),
])

green_schema = pa.schema([
    ("VendorID", pa.string()),
    ("lpep_pickup_datetime", pa.timestamp("s")),
    ("lpep_dropoff_datetime", pa.timestamp("s")),
    ("store_and_fwd_flag", pa.string()),
    ("RatecodeID", pa.string()),
    ("PULocationID", pa.string()),
    ("DOLocationID", pa.string()),
    ("passenger_count", pa.int64()),
    ("trip_distance", pa.decimal128(38, 9)),
    ("fare_amount", pa.decimal128(38, 9)),
    ("extra", pa.decimal128(38, 9)),
    ("mta_tax", pa.decimal128(38, 9)),
    ("tip_amount", pa.decimal128(38, 9)),
    ("tolls_amount", pa.decimal128(38, 9)),
    ("ehail_fee", pa.decimal128(38, 9)),
    ("improvement_surcharge", pa.decimal128(38, 9)),
    ("total_amount", pa.decimal128(38, 9)),
    ("payment_type", pa.int32()),
    ("trip_type", pa.string()),
    ("congestion_surcharge", pa.decimal128(38, 9)),
])


def download_file_parquet(service,year,month):
    url = f"{BASE_URL_PARQUET}{service}_tripdata_{year}-{month}.parquet"
    # file_path = os.path.join(DOWNLOAD_DIR, f"{service}_tripdata_{year}-{month}.parquet")
    file_path = Path(__file__).parent / f"{service}_tripdata_{year}-{month}.parquet"

    if Path(file_path).exists():
        print(f"The file {file_path} exists and was skipped.")
        return file_path

    try:
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, file_path)
        print(f"Downloaded: {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None
    
def download_file_csv(service,year,month):
    file_name = f"{service}_tripdata_{year}-{month}.csv.gz"
    url = f"{BASE_URL_CSV}{service}/{file_name}"
    # file_path = os.path.join(DOWNLOAD_DIR, f"{service}_tripdata_{year}-{month}.parquet")
    file_path = Path(__file__).parent / f"{service}_tripdata_{year}-{month}.parquet"
    
    if Path(file_path).exists():
        print(f"The file {file_path} exists and was skipped.")
        return file_path

    try:
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, Path(__file__).parent / file_name)
        print(f"Downloaded: {file_name}")
        
        # Read into parquet file using pandas
        df = pd.read_csv(Path(__file__).parent / file_name, compression='gzip')
        df.to_parquet(file_path, engine='pyarrow')
        print(f"Saved Parquet: {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None
    
def download_file(fmt,service,year,month):
    if fmt == 'csv':
        saved_file_path = download_file_csv(service,year,month)
    else:
        saved_file_path = download_file_parquet(service,year,month)
        
    return saved_file_path
        


def normalize_datatypes(trgt_schea,file_path):
    # destination = os.path.join(DOWNLOAD_DIR, f"{Path(file_path).stem}_normalized.parquet")
    destination = Path(__file__).parent / f"{Path(file_path).stem}_normalized.parquet"

    
    if Path(destination).exists():
        print(f"The file {destination} exists and was skipped.")
        return destination
    
    try:
        table = pq.read_table(file_path)
        cast_table = table.cast(target_schema = trgt_schea)
        pq.write_table(cast_table,destination)
        print(f"Saved normalized schema to: {destination}")
        return destination
    except Exception as e:
        print(f"Failed to normalize {file_path}: {e}")
        return None


def create_bucket(bucket_name):
    try:
        # Get bucket details
        bucket = client.get_bucket(bucket_name)

        # Check if the bucket belongs to the current project
        project_bucket_ids = [bckt.id for bckt in client.list_buckets()]
        if bucket_name in project_bucket_ids:
            print(
                f"Bucket '{bucket_name}' exists and belongs to your project. Proceeding..."
            )
        else:
            print(
                f"A bucket with the name '{bucket_name}' already exists, but it does not belong to your project."
            )
            sys.exit(1)

    except NotFound:
        # If the bucket doesn't exist, create it
        bucket = client.create_bucket(bucket_name)
        print(f"Created bucket '{bucket_name}'")
    except Forbidden:
        # If the request is forbidden, it means the bucket exists but you don't have access to see details
        print(
            f"A bucket with the name '{bucket_name}' exists, but it is not accessible. Bucket name is taken. Please try a different bucket name."
        )
        sys.exit(1)


def verify_gcs_upload(blob_name):
    return storage.Blob(bucket=bucket, name=blob_name).exists(client)


def upload_to_gcs(file_path, max_retries=3):
    blob_name = os.path.basename(file_path)
    blob = bucket.blob(blob_name)
    blob.chunk_size = CHUNK_SIZE

    for attempt in range(max_retries):
        try:
            print(f"Uploading {file_path} to {BUCKET_NAME} (Attempt {attempt + 1})...")
            blob.upload_from_filename(file_path)
            print(f"Uploaded: gs://{BUCKET_NAME}/{blob_name}")

            if verify_gcs_upload(blob_name):
                print(f"Verification successful for {blob_name}")
                return
            else:
                print(f"Verification failed for {blob_name}, retrying...")
        except Exception as e:
            print(f"Failed to upload {file_path} to GCS: {e}")

        time.sleep(5)

    print(f"Giving up on {file_path} after {max_retries} attempts.")


def get_args():
    parser = argparse.ArgumentParser(description='Run injection script for TLC taxi trip data.')
    parser.add_argument('--service', '-s', default='yellow', help='The service to injest - [yellow,green,fhv]')
    parser.add_argument('--year', '-y', default='2019', help='The year to injest')
    parser.add_argument('--fmt', '-f', default='parquet', help='The format to be downloaded - [parquet,csv]. If parquet the data will be downloaded from the NYC TLC website. Otherwise from the DataTalksClub repository.')
    
    return parser.parse_args()

def main(service,year,fmt) -> None: 
    create_bucket(BUCKET_NAME)

    # Change max workers if "Killed" because its caused from OOM.
    with ThreadPoolExecutor(max_workers=4) as executor:
        file_paths = list(executor.map(download_file, repeat(fmt),repeat(service),repeat(year),MONTHS))
            
    if service == 'fhv':
        target_schema = fhv_schema
    elif service == 'yellow':
        target_schema = yellow_schema
    else:
        target_schema = green_schema
    # Normalize the data
    with ThreadPoolExecutor(max_workers=4) as executor:
        file_paths = list(executor.map(normalize_datatypes,repeat(target_schema),file_paths))

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(upload_to_gcs, filter(None, file_paths))  # Remove None values

    print("All files processed and verified.")

if __name__ == "__main__":
    
    args = get_args()
    
    main(**vars(args))