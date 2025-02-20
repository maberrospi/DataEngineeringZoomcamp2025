import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# pandas_pq = pd.read_parquet("./fhv_tripdata_2024-01.parquet")
table = pq.read_table("./fhv_tripdata_2019-01_normalized.parquet")
print(table.schema)
# my_schema = pa.schema([
#     pa.field('dispatching_base_num',pa.string()),
#     pa.field("pickup_datetime",pa.timestamp('s')),
#     pa.field("dropOff_datetime",pa.timestamp('s')),
#     pa.field("PUlocationID",pa.int64()),
#     pa.field("DOlocationID",pa.int64()),
#     pa.field("SR_Flag",pa.int64()),
#     pa.field("Affiliated_base_number",pa.string())
# ])
# cast_table = table.cast(target_schema = my_schema)
# print(cast_table.schema)
# print(table['pickup_datetime'][:5])
# print(cast_table['pickup_datetime'][:5])
# pq.write_table(cast_table,'test_transf.parquet')

# # Check the cast was succesful

# new_table = pq.read_table('test_transf.parquet')
# print(new_table.schema)
# print(new_table['pickup_datetime'][:5])

# print(pandas_pq.head(5))
# print(pandas_pq.dtypes)