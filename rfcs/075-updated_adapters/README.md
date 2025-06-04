
# RFC 075: Using Apache Iceberg tables in Catalogue Pipeline adapters

Discussing a replacement architecture for the catalogue pipeline adapters, moving away from the Versioned Hybrid Store (VHS) using Apache Iceberg as the underlying storage format.

**Last modified:** 2025-06-02T14:01:45Z

## Table of contents

- [Context](#context)
    - [Required functionality of adapters](#required-functionality-of-adapters)
    - [Current architecture overview](#current-architecture)
    - [Problems with current architecture](#problems-with-current-architecture)
    - [Other considerations](#other-considerations)
- [Proposal](#proposal)
  - [Scalability testing](#scalability-testing)
  - [New adapter architecture using iceberg](#new-adapter-architecture-using-iceberg)
- [Impact](#impact)
- [Next steps](#next-steps)

## Context

The function of "adapters" in the catalogue pipeline is to provide a standard interface for the rest of the catalogue pipeline to act on data from source systems without direct concern for the load or availability of those systems. See this [description of adapters in the pipeline](https://docs.wellcomecollection.org/catalogue-pipeline/fetching-records-from-source-catalogues/what-is-an-adapter).

An adapter decouples synchronizing changes from a source system, with the process of transforming, matching and merging that happen later in the pipeline. An adapter can be thought of as serving 4 main purposes:

### Required functionality of adapters

- Noticing and fetching changes from a source system.
- Writing changes to a storage system, which can be queried later.
- Notifying the rest of the pipeline that changes have occurred, so that they can be processed.
- During a reindex, notifying the rest of the pipeline about the current state of the source system, so that it can be transformed and indexed in totality.

### Current architecture overview

The current adapters use a Versioned Hybrid Store (VHS) to store data from source systems, which is a custom storage format that provides versioning and schema-less data storage. This has worked well for many years, but has some drawbacks that we want to address.

See this blog post on the [Versioned Hybrid Store (VHS)](https://stacks.wellcomecollection.org/creating-a-data-store-from-s3-and-dynamodb-8bb9ecce8fc1) for more information about the current implementation. In summary the VHS is a custom storage format that combines S3 and an index in DynamoDB to provide a versioned, schema-less data store that can be queried on the id and version of a record. 

The VHS allows for storing multiple versions of a record, and was originally designed to overcome the limitations of S3 as a data store, which did not at the time provide [read after write consistency](https://aws.amazon.com/blogs/aws/amazon-s3-update-strong-read-after-write-consistency/).

The current architecture consists of several components:

- **Window generators**: This is a service that generates time windows for processing data from source systems. Windows are sent to adapters to fetch changes from source systems within a given time window. It can be used to control the frequency of updates from source systems, and to track missing completed windows.
- **Adapters**: These are services that fetch changes from source systems and write them to the Versioned Hybrid Store (VHS). They also notify the rest of the pipeline about changes.
- **Reindexer**: This is a service that understands how to query the VHS and generates upstream notifications for the rest of the pipeline. It is used to reindex data from source systems when necessary, e.g. when the `Work` model changes and we need to re-transform and reindex all data.

#### Relationship to the Work model

The granularity of the data stored in the VHS is at the level of individual records, that can be transformed into the `Work` model. The VHS stores data in a schema-less format, which allows for flexibility in the data model, but also means that we have to handle schema changes upstream in the source systems. 

Transformer services read data from the VHS, transforms it into a format suitable for indexing, and writes it to Elasticsearch. 

Notifications from the adapters are used to trigger the transformers to process data, this happens in a "push" model where the adapters notify the transformers about changes to individual records via SNS/SQS.

### Problems with current architecture

There are several problems with the current architecture that we want to address, apart from updating the design to use more modern technologies and without the need to work around previous limitations of S3.

1. **Keeping unused versions**: The VHS retains all versions of a record, however we do not make use of the versioning functionality in the VHS, there is no mechanism for accessing old versions, and there is no provision for cleaning up old versions of records. This has resulted in large amounts of unused data being stored, which is costly.

2. **Difficult to inspect source data**: As records are stored in S3 with an index in DynamoDB and the data stored in S3 is scheme-less, it is difficult to inspect the source data directly and understand its structure and contents in aggregate. 

3. **Novel approach, difficult to understand**: The VHS is a custom storage format that is not  used outside of Wellcome Collection, which makes it difficult for new developers to understand and work with. It also means that we have to maintain our own custom code for reading and writing data, which adds complexity.

4. **Schema-less data storage**: The VHS allows for schema-less data storage, which means that we do not enforce a schema on the data stored in the VHS. This can lead to issues with data quality and consistency, as we do not have a mechanism for validating the structure of the data before it is written to the store. While this has allowed us to handle changes in source systems more easily, it has also led to records of the same data model having different structures.

   Although data stored in the VHS is schema-less transformers are responsible for decoding source data, and reference source data types in their code. This means that if a source system changes its schema, we have to update the transformers to handle the new schema in any case, negating some of the benefits of schema-less storage.

### Other considerations

The ongoing Wellcome Collection Systems Transformation Project (WCSTP) aims to replace the current Library Management System (LMS) and Collection Management System (CMS). This will involve rewriting the adapters for these systems, which provides an opportunity to update the architecture of the adapters to use more modern technologies and approaches.

We are in the process of moving to use Lambda functions for many of our catalogue pipeline components, in order to reduce infrastructure management overhead and improve scalability, and to do so using Python as the primary language for development. We will need to ensure that the new adapter architecture is compatible with this approach.

Recent development of the catalogue graph discussed in other RFCS [RFC 066: Catalogue Graph](https://github.com/wellcomecollection/docs/tree/main/rfcs/066-graph_pipeline) has shown that we can use AWS Step Functions to orchestrate complex workflows, which could be used to manage the flow of data through the adapters and transformers.

## Proposal 
    to use apache iceberg

    what is it?
        discuss parquet
        discuss iceberg tables
    why is it suited to this problem?
        good compression
        ACID transactions
        support in tooling (python, polars, duckdb but also spark)
        support in data engineering community
        support in AWS:
            S3 Tables
            Glue Catalog 
            querying using Athena

### Scalability testing
    why?
        discuss what is happening when queries and upserts occur
        relationship to table clean-up operations

    loading calm and sierra data to iceberg tables
    testing querying and upsert performance from 

    reproduce: 
        https://github.com/wellcomecollection/platform/issues/6030
        https://github.com/wellcomecollection/platform/issues/6029 
        
### New adapter architecture using iceberg

    What might things look like if we used Iceberg:

    #### Use of AWS Step Functions
        success in catalogue graph project, 
        how often might updates propagate? should aim for 15 minutes?
        adapters will write iceberg table
        transformers will read iceberg table 
        transformers will continue to write to ES (for now)

    #### Use of Lambda / ECS Tasks
        python lambdas where possible
        ECS tasks if we exceed time limits
        both can be orchestrated using step functions (examples in catalogue graph project)

    #### Use of S3 Tables
        provides table clean up, optimised for performance
        how this works
            provides iceberg REST API, get object only

    #### Iceberg Table Configuration
        cleaning up table snapshots
        table partitions for optimal performance

    #### Reproducing reindexer functionality
        new reindexer can query iceberg tables
        standard parts of schema required for this

## Alternatives considered
    why we might use it, why it's not suitable

    monolithic parquet file
    manual sharding in parquet
    file per source work
    using plain S3 buckets with Iceberg

## Impact
    easier to query source data
    schema required for source data in adapter
    reduction in catalogue data pipeline novelty
    potentially cheaper with reduced storage requirements (storing all versions at the moment)
    simpler from architecture perspective
    
    diverse adapters (we'll need to accomodate both approaches as we switch over)

## Next steps
    move an existing adapter over to familiarise ourselves further and test in production?
    begin implementation for new CMS?
    