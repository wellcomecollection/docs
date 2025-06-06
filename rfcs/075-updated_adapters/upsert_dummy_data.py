# %%
from pyiceberg.catalog import load_catalog

import os

s3_tables_bucket = "calm-tech-spike"
namespace = "calm_adapter_test"
catalog_name = "s3tablescatalog"
table_name = "test_table"

full_table_name = f"{namespace}.{table_name}"

# Set the environment variable for the AWS credentials
os.environ["AWS_PROFILE"] = "platform-developer"

catalog = load_catalog(
  catalog_name,
  **{
    "type": "rest",    
    "warehouse": f"123497843905:s3tablescatalog/{s3_tables_bucket}",
    "uri": f"https://glue.eu-west-1.amazonaws.com/iceberg",
    "rest.sigv4-enabled": "true",
    "rest.signing-name": "glue",
    "rest.signing-region": "eu-west-1",
  }
)

# %%
catalog.create_namespace(namespace)
ns = catalog.list_namespaces()
ns

# %%
from pyiceberg.schema import Schema, NestedField, IntegerType, StringType, TimestampType
from pyiceberg.partitioning import PartitionSpec, PartitionField
from pyiceberg.transforms import BucketTransform, DayTransform
import polars as pl
import pyarrow as pa

schema = Schema(
    NestedField(1, "id", IntegerType(), required=True),
    NestedField(2, "name", StringType(), required=False),
    NestedField(3, "message", StringType(), required=True),
    # last modified field
    NestedField(4, "last_modified", TimestampType(), required=True),
    identifier_field_ids=[1]  # 'id' is the primary key
)

partition_spec = PartitionSpec(
    fields=[
        PartitionField(source_id=1, field_id=1000, transform=BucketTransform(num_buckets=10), name="id"),
        PartitionField(source_id=4, field_id=1001, transform=DayTransform(), name="last_modified")
    ]
)

pa_schema = schema.as_arrow()
pl_schema = pl.from_arrow(pa_schema.empty_table()).schema 

def create_polars_df(data):
    df = pl.DataFrame(
        data=data,
        schema=pl_schema
    )
    return df

def polars_to_arrow(df):
    return pa.Table.from_pandas(
        df.to_pandas(), 
        schema=pa_schema
    )

schema

# %%
table = catalog.create_table(
    identifier=full_table_name,
    schema=schema,
    partition_spec=partition_spec
)

catalog.list_tables(namespace)

# %%
table

# %%
import polars as pl

# create a dataframe with 10k random rows

import datetime
import random

data = []

for i in range(1000000):
    # generate random data for the above schema
    id_value = i
    name_value = f"name_{i}" if random.random() > 0.1 else None  # 10% chance of being None
    message_value = f"message_{i}"
    data.append({
        "id": id_value,
        "name": name_value,
        "message": message_value,
        "last_modified": datetime.datetime.now(datetime.timezone.utc)
    })

pl_df = create_polars_df(data)
pa_df = polars_to_arrow(pl_df)

# %%
# get the table
table = catalog.load_table(full_table_name)
table

# %%
table.append(pa_df)

# %%
conn = table.scan().to_duckdb(table_name)
# results = conn.sql(f"SELECT * FROM {table_name} WHERE id = 145 OR id = 120 LIMIT 5")

results = conn.sql(f"SELECT * FROM {table_name} WHERE " + " OR ".join([f"id = {i}" for i in range(1000)]))

results.show()

# %%
# generate 100 records to upsert at random ids (1-1000000), ensure the id field is unique
import random
 
def generate_upsert_dataset(length, range_size=1000000):
    upsert_data = []   

    # randomise the order of IDs to ensure randomness
    existing_ids = range(range_size) # IDs from the original dataset
    existing_ids = random.sample(existing_ids, len(existing_ids))

    # pick length ids from the start of existing_ids
    ids_to_generate = existing_ids[:length]

    for id_value in ids_to_generate:
        name_value = f"name_{id_value}" if random.random() > 0.1 else None
        message_value = f"upsert_message_{id_value}"
        upsert_data.append({
            "id": id_value,
            "name": name_value,
            "message": message_value,
            "last_modified": datetime.datetime.now(datetime.timezone.utc)
        })

    upsert_df = create_polars_df(upsert_data)
    upsert_pa_df = polars_to_arrow(upsert_df)

    return upsert_pa_df


# %%
# generate upsert datasets in orders of magnitude from 1 to 1000000, perform upserts and measure time taken, print the result

import time

for length in [1, 10, 100, 1000, 10000, 100000, 1000000]:
    upsert_pa_df = generate_upsert_dataset(length)
    print(f"Upserting {length} records...")
    start_time = time.time()
    table.upsert(upsert_pa_df)
    end_time = time.time()
    
    print(f"Upserted {length} records in {end_time - start_time:.2f} seconds")


# %%
namespaces = catalog.list_namespaces()
print(f"Namespaces in the catalog: {namespaces}")
for ns in namespaces:
    for table in catalog.list_tables(ns):
        print(f"Table in namespace {ns}: {table}")

full_table_name = f"{namespace}.{table_name}"
if len(namespaces) > 0 and (namespace, table_name) in catalog.list_tables(namespace):
    catalog.purge_table(
        identifier=full_table_name
    )
    print(f"Table {full_table_name} purged successfully.")
else:
    print(f"Table {full_table_name} does not exist.")

if (namespace,) in catalog.list_namespaces():
    catalog.drop_namespace(
        namespace=namespace,
    )
    print(f"Namespace {namespace} deleted successfully.")
else:
    print(f"Namespace {namespace} does not exist.")

# %%