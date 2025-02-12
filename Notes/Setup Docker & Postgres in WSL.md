## Run Postgres and PgAdmin

### Create a network to connect them

```
docker network create pg-network
```

### Create Volume

```
docker volume create --name dtc_postgres_volume_local -d local
```
### Run Postgres container

```
docker run -it   -e POSTGRES_USER="root"   -e POSTGRES_PASSWORD="root"   -e POSTGRES_DB="ny_taxi"   -v dtc_postgres_volume_local:/var/lib/postgresql/data   -p 5432:5432 --network=pg-network --name pg-database   postgres:13
```
### Run PgAdmin container

```
docker run -it   -e PGADMIN_DEFAULT_EMAIL="admin@admin.com"   -e PGADMIN_DEFAULT_PASSWORD="root"   -p 8080:80   --network=pg-network   --name pgadmin   dpage/pgadmin4
```


### Install pgcli (Optional)

`sudo apt install pgcli` -> Use this is `pip install pgcli` isn't allowed.

### Connect to postgress using CLI (Optional)

```
pgcli -h localhost -p 5432 -u root -d ny_taxi
```
## Ingest Data

### Create the Dockerfile for the ingestion pipeline

```
FROM python:3.9.1

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app

COPY ingest_data.py ingest_data.py  

ENTRYPOINT [ "python", "ingest_data.py" ]
```
### Build the ingestion pipeline image

```
docker build -t taxi_ingest:v001 .
```

In CMD run:
`
```
wsl@user:/mnt/c/Users/user/Desktop/DataEngineeringZoomcamp2025/ZoomcampFiles$ URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"`
```

```
wsl@user:/mnt/c/Users/user/Desktop/DataEngineeringZoomcamp2025/ZoomcampFiles$ docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}```
```

## Use docker-compose for future runs

### Create docker-compose.yaml file

```
services:
  pgdatabase:
    image: postgres:13
    environment:
      - POSTGRES_USER=root
      - POSTGRES_PASSWORD=root
      - POSTGRES_DB=ny_taxi
    volumes:
      - "dtc_postgres_volume_local:/var/lib/postgresql/data:rw"
    ports:
      - "5432:5432"

  pgadmin:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=root
    ports:
      - "8080:80"
volumes:
  dtc_postgres_volume_local:
    external: true
```

### Run containers using this yaml file

```
docker compose up
```

### Inspect data in PgAdmin web

```
Go to http://localhost:8080/

Login using credentials found in .yaml file
```


#### Additional Info

The docker volume was created at `dtc_postgres_volume_local`

The following command show the location of this volume. This locations is NOT meant to be accessed or modified. According to the instructions we should have a folder `ny_taxi_postgres_data` but using the commands above this volume is created elsewhere and the folder remains empty.

```
docker volume inspect dtc_postgres_volume_local
[
    {
        "CreatedAt": "2025-02-04T09:48:13Z",
        "Driver": "local",
        "Labels": null,
        "Mountpoint": "/var/lib/docker/volumes/dtc_postgres_volume_local/_data",
        "Name": "dtc_postgres_volume_local",
        "Options": null,
        "Scope": "local"
    }
]
```
