# %%
# using boto3 create a session using the "platform-developer" profile
import boto3

def create_session(profile_name='platform-developer'):
    """
    Create a boto3 session using the specified profile name.
    
    :param profile_name: The name of the AWS profile to use.
    :return: A boto3 session object.
    """
    session = boto3.Session(profile_name=profile_name)
    return session

# create a dynamo client from a session

def create_dynamo_client(session):
    """
    Create a DynamoDB client from the provided boto3 session.
    
    :param session: A boto3 session object.
    :return: A DynamoDB client object.
    """
    dynamo_client = session.client('dynamodb')
    return dynamo_client

def create_s3_client(session):
    """
    Create an S3 client from the provided boto3 session.
    
    :param session: A boto3 session object.
    :return: An S3 client object.
    """
    s3_client = session.client('s3')
    return s3_client

# %%
dynamo_client = create_dynamo_client(create_session())


# %%
# example record:
# {'id': {'S': 'cb41c0ba-5d4c-482b-98f8-285f993f4f12'},
#  'payload': {'M': {'bucket': {'S': 'wellcomecollection-vhs-calm-adapter'},
#    'key': {'S': 'cb41c0ba-5d4c-482b-98f8-285f993f4f12/11/e17627d2-49cd-4a03-929b-4474715117cd.json'}}},
#  'version': {'N': '11'}}

# scan the table and assemble a list of records

import json

def scan_table(dynamo_client, table_name):
    """
    Scan the specified DynamoDB table and return all records.
    
    :param table_name: The name of the DynamoDB table to scan.
    :return: A list of records from the table.
    """
    response = dynamo_client.scan(TableName=table_name)
    items = response.get('Items', [])

    for item in items:
        yield json.dumps(item)
    
    # Handle pagination if there are more items
    while 'LastEvaluatedKey' in response:
        response = dynamo_client.scan(TableName=table_name, ExclusiveStartKey=response['LastEvaluatedKey'])
        items = response.get('Items', [])
        
        for item in items:
            yield json.dumps(item)
    

# %%
# dump the records to a file 

def dump_records_to_file(base_dir, table_name):
    dynamo_client = create_dynamo_client(create_session())
    filename=f"{base_dir}/dynamo_dump_{table_name}.jsonl"

    # append the records to a file

    with open(filename, 'a') as f:
        for item in scan_table(dynamo_client, table_name):
            f.write(f"{item}\n")

# %%

import os

def _convert_to_s3_location(record):
    bucket = record['payload']['M']['bucket']['S']
    key = record['payload']['M']['key']['S']
    return f's3://{bucket}/{key}'

def download_record(s3_client, record, data_dir):
    """
    Download a record from S3 based on the provided record.
    
    :param s3_client: An S3 client object.
    :param record: A DynamoDB record in JSON format.
    :return: None
    """
    s3_location = _convert_to_s3_location(record)
    bucket = s3_location.split('/')[2]
    key = '/'.join(s3_location.split('/')[3:])

    # check if file exists before downloading
    if not os.path.exists(f"{data_dir}/{record['id']['S']}.json"):
        s3_client.download_file(
            Bucket=bucket,
            Key=key,
            Filename=f"{data_dir}/{record['id']['S']}.json"
        )

# %%
# read the data dump and download the records

import json

def download_records_from_dump(table_name, data_dir):
    with open(f"./data/dynamo_dump_{table_name}.jsonl", 'r') as f:
        dynamo_client = create_dynamo_client(create_session())
        s3_client = create_s3_client(create_session())
        
        import concurrent.futures

        # check if the directory exists, if not create it
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for line in f:
                record = json.loads(line)
                futures.append(executor.submit(download_record, s3_client, record, data_dir))
            
            # wait for all futures to complete
            concurrent.futures.wait(futures)
            # close the executor
            executor.shutdown(wait=True)


# %%
# table_name = 'vhs-calm-adapter'
table_name = 'vhs-sierra-sierra-adapter-20200604'
base_dir = "./data"
data_dir = f"{base_dir}/{table_name}"

# dump_records_to_file(base_dir, table_name)
# download_records_from_dump(table_name, data_dir)

# %%
# open ./data/vhs-sierra-sierra-adapter-20200604/1007580.json and parse the json
import json
import pyarrow as pa

# example usage
sample_sierra_file_path = './data/vhs-sierra-sierra-adapter-20200604/1007580.json'
sample_sierra_json_data = None
with open(sample_sierra_file_path, 'r') as f:
        sample_sierra_json_data = json.load(f)

# infer an iceberg schema from the json
from pyiceberg.schema import Schema, NestedField
from pyiceberg.partitioning import PartitionSpec, PartitionField
from pyiceberg.transforms import BucketTransform
from pyiceberg.types import (
    StringType,
    ListType,
    MapType,
    TimestampType,
    StructType,
)

def make_record_map_type(base_field_id, base_element_id):
    """
    Helper to generate a MapType for item_records, holdings_records, or order_records.
    Ensures unique field_ids and element_ids for each usage.
    """
    return MapType(
        key_id=base_field_id + 100,  # must be unique and int
        value_id=base_field_id + 200,  # must be unique and int
        key_type=StringType(),
        value_type=StructType(
            NestedField(field_id=base_field_id + 0, name="id", field_type=StringType(), required=False),
            NestedField(field_id=base_field_id + 1, name="data", field_type=StringType(), required=False),
            NestedField(field_id=base_field_id + 2, name="modified_date", field_type=TimestampType(), required=False),
            NestedField(field_id=base_field_id + 3, name="bib_ids", field_type=ListType(element_id=base_element_id + 0, element_type=StringType(), element_required=False), required=False),
            NestedField(field_id=base_field_id + 4, name="unlinked_bib_ids", field_type=ListType(element_id=base_element_id + 1, element_type=StringType(), element_required=False), required=False),
        )
    )

sierra_iceberg_schema = Schema(
    NestedField(
        field_id=1,
        name="id",
        field_type=StringType(),
        required=True
    ),
    NestedField(
        field_id=2,
        name="maybe_bib_record",
        field_type=StructType(
            NestedField(field_id=21, name="id", field_type=StringType(), required=False),
            NestedField(field_id=22, name="data", field_type=StringType(), required=False),
            NestedField(field_id=23, name="modified_date", field_type=TimestampType(), required=False),
        ),
        required=False
    ),
    NestedField(
        field_id=3,
        name="item_records",
        field_type=make_record_map_type(31, 340),
        required=True
    ),
    NestedField(
        field_id=4,
        name="holdings_records",
        field_type=make_record_map_type(41, 440),
        required=True
    ),
    NestedField(
        field_id=5,
        name="order_records",
        field_type=make_record_map_type(51, 540),
        required=True
    ),
    NestedField(
        field_id=6,
        name="modified_time",
        field_type=TimestampType(),
        required=True
    ),
    identifier_field_ids=[1]
)

sierra_iceberg_partition_spec = PartitionSpec(
    fields=[
        PartitionField(source_id=1, field_id=1000, transform=BucketTransform(num_buckets=100), name="id"),
    ]
)


from pyiceberg.io.pyarrow import schema_to_pyarrow as iceberg_to_arrow_schema

sierra_schema = iceberg_to_arrow_schema(sierra_iceberg_schema, include_field_ids=False)

# transform the dict into a format that can be used to create a pyarrow table

from datetime import datetime

def parse_iso_or_none(val):
    if not val:
        return None
    try:
        return datetime.fromisoformat(val.replace("Z", "+00:00"))
    except Exception:
        return None
    
def transform_sierra_id(maybe_id):
    if maybe_id is not None:
        # We have a mixture of at least three different JSON encodings in the pipeline:
        #
        #  - as a String
        #  - as an Int
        #  - as a JSON object {"recordNumber": "1234567"}
        # 
        # We want to ensure that we always return a String
        # Otherwise throw an error
        if isinstance(maybe_id, int):
            maybe_id = str(maybe_id)
        elif isinstance(maybe_id, dict):
            maybe_id = maybe_id.get("recordNumber", None)
            if maybe_id is not None:
                maybe_id = str(maybe_id)
        elif not isinstance(maybe_id, str):
            raise ValueError(f"Invalid sierraId format: {maybe_id}")

    return maybe_id

def transform_sierra_data(data_as_dict):
    return {
        "id": transform_sierra_id(data_as_dict["sierraId"]),
        "maybe_bib_record": {
            "id": transform_sierra_id(data_as_dict["maybeBibRecord"]["id"]),
            "data": data_as_dict["maybeBibRecord"]["data"],
            "modified_date": parse_iso_or_none(data_as_dict["maybeBibRecord"]["modifiedDate"])
        } if data_as_dict.get("maybeBibRecord") else None,
        "item_records": {
            k: {
                "id": transform_sierra_id(v["id"]),
                "data": v["data"],
                "modified_date": parse_iso_or_none(v["modifiedDate"]),
                "bib_ids": v.get("bibIds", []),
                "unlinked_bib_ids": v.get("unlinkedBibIds", [])
            }
            for k, v in data_as_dict.get("itemRecords", {}).items()
        },
        "holdings_records": {
            k: {
                "id": transform_sierra_id(v["id"]),
                "data": v["data"],
                "modified_date": parse_iso_or_none(v["modifiedDate"]),
                "bib_ids": v.get("bibIds", []),
                "unlinked_bib_ids": v.get("unlinkedBibIds", [])
            }
            for k, v in data_as_dict.get("holdingsRecords", {}).items()
        },
        "order_records": {
            k: {
                "id": transform_sierra_id(v["id"]),
                "data": v["data"],
                "modified_date": parse_iso_or_none(v["modifiedDate"]),
                "bib_ids": v.get("bibIds", []),
                "unlinked_bib_ids": v.get("unlinkedBibIds", [])
            }
            for k, v in data_as_dict.get("orderRecords", {}).items()
        },
        "modified_time": parse_iso_or_none(data_as_dict["modifiedTime"])
    }


transformed_sierra_sample_record = transform_sierra_data(sample_sierra_json_data)
sample_sierra_pa_table = pa.Table.from_pylist([transformed_sierra_sample_record], schema=sierra_schema)

# load the table as a polars df and show it

import polars as pl

pl_df = pl.from_arrow(sample_sierra_pa_table)
print(pl_df)



# %%
from datetime import datetime

from pyiceberg.schema import Schema, NestedField, BooleanType, StringType, TimestampType, StructType, ListType
from pyiceberg.partitioning import PartitionSpec, PartitionField
from pyiceberg.transforms import BucketTransform, DayTransform

calm_data_fields = [
   'UserText2', 'Link_To_Digitised', 'Appraisal', 'Level', 'Location', 'Format',
    'PreviousNumbers', 'UserWrapped5', 'UserText7', 'Created', 'UserWrapped6',
    'CountryCode', 'UserText3', 'Title', 'ACCESS', 'Arrangement', 'CustodialHistory',
    'SDB_Type', 'CONTENT', 'Inscription', 'SDB_Ref', 'Transmission', 'AccessStatus',
    'TargetAudience', 'Condition', 'CreatorName', 'CONSERVATIONREQUIRED', 'Format_Details',
    'UserWrapped2', 'Digital_Date_Created', 'UserText9', 'Copyright_Expiry', 'Accruals',
    'Material', 'Description', 'Acquisition', 'UserText8', 'AccessCategory',
    'Digitised', 'UserText4', 'Modifier', 'Copyright', 'UserDate1', 'ClosedUntil',
    'Ordering_Status', 'Digital_Last_Modified', 'Bnumber', 'Creator', 'ConservationStatus',
    'AV_Timecode', 'MISC_Reference', 'Language', 'IDENTITY', 'RCN', 'Producible_Unit',
    'RelatedMaterial', 'Digital_File_Path', 'UserText5', 'Access_Licence',
    'Sources_Guides_Used', 'RefNo', 'ExitNote', 'UserWrapped4', 'AccessConditions',
    'RepositoryCode', 'UserWrapped7', 'CONTEXT', 'Digital_File_Format', 'Data_Import_Landing',
    'ALLIED_MATERIALS', 'Date', 'ConservationPriority', 'Originals', 'Notes',
    'Metadata_Licence', 'UserText6', 'AV_Target_Audience_Details', 'Extent', 'AltRefNo',
    'RecordID', 'RecordType', 'Player_Code', 'SDB_URL', 'UserWrapped3', 'PublnNote',
    'UserWrapped8', 'Credits', 'CatalogueStatus', 'AdminHistory', 'Copies', 'Modified',
    'Document'
]

# reproduce the schema in Iceberg

# Starting field_id for fields within the 'data' struct.
# Ensure this range doesn't overlap with top-level field_ids.
# We also need unique element_ids for the ListType.
# Let's assign field_ids from 100 onwards, and element_ids from 1000 onwards.
next_data_field_id = 100
next_element_id = 1000 # For elements within ListType

data_fields_list = []
for field_name in calm_data_fields:
    current_field_id = next_data_field_id
    current_element_id = next_element_id
    next_data_field_id += 1
    next_element_id +=1

    data_fields_list.append(
        NestedField(
            field_id=current_field_id,
            name=field_name,
            field_type=ListType(
                element_id=current_element_id,
                element_type=StringType(),
                element_required=False
            ),
            required=False # Assuming the list field itself is optional
        )
    )

# Construct the StructType for 'data' using the generated list of NestedFields
data_schema = StructType(*data_fields_list)

# Define the main schema using the compacted data_schema
calm_iceberg_schema = Schema(
    NestedField(field_id=1, name="id", field_type=StringType(), required=True),
    NestedField(field_id=2, name="data", field_type=data_schema, required=False),
    NestedField(field_id=3, name="retrieved_at", field_type=TimestampType(), required=False),
    NestedField(field_id=4, name="published", field_type=BooleanType(), required=False),
    identifier_field_ids=[1] # Assign a schema ID as a list
)

# bucket partition on id into 100 buckets
calm_iceberg_partition_spec = PartitionSpec(
    fields=[
        PartitionField(source_id=1, field_id=1000, transform=BucketTransform(num_buckets=100), name="id"),
        # PartitionField(source_id=3, field_id=1001, transform=DayTransform(), name="retrieved_at"),
    ]
)

from pyiceberg.io.pyarrow import schema_to_pyarrow as iceberg_to_arrow_schema

calm_schema = iceberg_to_arrow_schema(calm_iceberg_schema, include_field_ids=False)

def transform_calm_data(data_as_dict):
    return {
        'id': data_as_dict['id'],
        'data': data_as_dict['data'],
        'retrieved_at': datetime.fromisoformat(data_as_dict['retrievedAt']),
        'published': data_as_dict.get('published', None)  # Use .get() to handle missing keys
    }

# %%
# load all the data from the data directory into a pyarrow table, using threads for both loading and transforming, with progress reporting

import os
import concurrent.futures
import pyarrow as pa

def load_and_transform_data_to_arrow_table(data_dir, transform, schema):
    """
    Load and transform all the JSON files in the given directory into a PyArrow table, using threads and reporting progress.
    """
    import time

    def load_and_transform(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        return transform(data)

    json_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.json')]
    total = len(json_files)
    print(f"Found {total} JSON files in {data_dir}")

    transformed_data = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_file = {executor.submit(load_and_transform, file): file for file in json_files}
        for idx, future in enumerate(concurrent.futures.as_completed(future_to_file), 1):
            file = future_to_file[future]
            try:
                record = future.result()
                transformed_data.append(record)
            except Exception as e:
                print(f"Error loading or transforming {file}: {e}")
                continue
            if idx % 100 == 0 or idx == total:
                print(f"Processed {idx}/{total} files")

    print("All files loaded and transformed, building Arrow table...")

    try:
        table = pa.Table.from_pylist(transformed_data, schema=schema)
    except Exception as e:
        print("Error converting to Arrow table. Attempting to find problematic record...")
        for i, record in enumerate(transformed_data):
            try:
                pa.Table.from_pylist([record], schema=schema)
            except Exception as rec_e:
                print(f"Problematic record at index {i}:")
                print(record)
                print("Error:", rec_e)
                if i > 0:
                    print("Previous record:")
                    print(transformed_data[i - 1])
                raise
        raise e

    return table

# %%
loaded_table = load_and_transform_data_to_arrow_table(data_dir, transform_sierra_data, sierra_schema)
# loaded_table = load_and_transform_data_to_arrow_table(data_dir, transform_calm_data, calm_schema)

# %%
# print how many records are in the table, and the first 10 records

print(f"Number of records in the table: {loaded_table.num_rows}")
print("First 10 records:")
for i in range(10):
    print(loaded_table.slice(i, 1).to_pylist()[0])

# %%
# Write the table to a parquet file
import pyarrow.parquet as pq

pq.write_table(loaded_table, f"{base_dir}/{table_name}.parquet")
print(f"Table written to {base_dir}/{table_name}.parquet")

# %%
import polars as pl

parquet_filename = f"{base_dir}/{table_name}.parquet"
pl_df = pl.read_parquet(parquet_filename)

# convert to a pyarrow table
reload_table = pl_df.to_arrow()

# %%
# print how many records are in the table, and the fitst 10 records
print(f"Number of records in the loaded table: {reload_table.num_rows}")
print("First 10 records from the loaded table:")
for i in range(10):
    print(reload_table.slice(i, 1).to_pylist()[0])

# %%

# lowercase and spaces / hyphens to underscores
import re

iceberg_table_name = re.sub(r'[^a-zA-Z0-9]', '_', table_name.lower())

if table_name == 'vhs-sierra-sierra-adapter-20200604':
    iceberg_schema = sierra_iceberg_schema
    iceberg_partition_spec = sierra_iceberg_partition_spec
elif table_name == 'vhs-calm-adapter':
    iceberg_schema = sierra_iceberg_schema
    iceberg_partition_spec = calm_iceberg_partition_spec

# %%
from pyiceberg.catalog import load_catalog

import os

s3_tables_bucket = "pipeline-adapter-dumps"
namespace = "adapter_dumps"
catalog_name = "s3tablescatalog"

full_table_name = f"{namespace}.{iceberg_table_name}"

# Set the environment variable for the AWS credentials
os.environ["AWS_PROFILE"] = "platform-developer"

catalog = load_catalog(
  catalog_name,
  **{
    "type": "rest",    
    "warehouse": f"760097843905:s3tablescatalog/{s3_tables_bucket}",
    "uri": f"https://glue.eu-west-1.amazonaws.com/iceberg",
    "rest.sigv4-enabled": "true",
    "rest.signing-name": "glue",
    "rest.signing-region": "eu-west-1",
  }
)

print(f"Working with table {full_table_name} in catalog {catalog_name}")

# %%
catalog.create_namespace(namespace)
ns = catalog.list_namespaces()
ns

# %%
table = catalog.create_table(
    identifier=full_table_name,
    schema=iceberg_schema,
    partition_spec=iceberg_partition_spec,
)

catalog.list_tables(namespace)

# %%
# get the table
catalog_table = catalog.load_table(full_table_name)
catalog_table

# %%
catalog_table.append(loaded_table)

# %%
conn = catalog_table.scan().to_duckdb(iceberg_table_name)

ids = [str(int(1623354) + i) for i in range(100)]

results = conn.sql(f"SELECT * FROM {iceberg_table_name} where id in ({','.join(ids)})")

results.show()

# %%
# query the catalog table using polars for the number of records

import polars as pl

pl.Config.set_verbose(True) 

iceberg_df = pl.scan_iceberg(catalog_table)

# get the records with ids

iceberg_df = iceberg_df.filter(pl.col("id").is_in(ids))
iceberg_df = iceberg_df.collect()

# show the first 10

print(iceberg_df.head(10))


# %%
namespaces = catalog.list_namespaces()
print(f"Namespaces in the catalog: {namespaces}")
for ns in namespaces:
    for table in catalog.list_tables(ns):
        print(f"Table in namespace {ns}: {table}")



# %%
if len(namespaces) > 0 and (namespace, iceberg_table_name) in catalog.list_tables(namespace):
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



