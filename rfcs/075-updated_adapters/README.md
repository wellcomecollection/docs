
# RFC 075: Using Apache Iceberg tables in Catalogue Pipeline adapters

Discussing a replacement architecture for the catalogue pipeline adapters, moving away from the Versioned Hybrid Store (VHS) using Apache Iceberg as the underlying storage format.

**Last modified:** 2025-06-02T14:01:45Z

## Table of contents

- [Context](#context)
    - [Required functionality of adapters](#required-functionality-of-adapters)
    - [Current architecture](#current-architecture)
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

### Current architecture

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

## Problems with current architecture


    problems with current approach
        keeping unused version
        difficult to inspect source data
        novel approach, difficult to understand

        schema-less data in source tables, we catch issues upstream 
            potential benefits drawbacks of not enforcing schema here 
            (if source schema changes we don't care, but we would still have to implement changes upstream)
            where do we enforce schema now?, what does it look like?

    systems transformation project and requirement for major adapter rewrite

    move to lambdas, and use of python

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
    