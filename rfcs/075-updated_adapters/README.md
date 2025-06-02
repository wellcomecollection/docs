
# RFC 075: Updated catalogue pipeline adapters

Discussing a replacement architecture for the catalogue pipeline adapters, moving away from the Versioned Hybrid Store (VHS) using Apache Iceberg as the underlying storage format.

**Last modified:** 2025-06-02T14:01:45Z

## Table of contents

- [Context](#context)
- [Proposal](#proposal)
  - [Scalability testing](#scalability-testing)
  - [New adapter architecture using iceberg](#new-adapter-architecture-using-iceberg)
- [Impact](#impact)
- [Next steps](#next-steps)

## Context
    what we have now, with relationship to reindexer
        versioned hybrid store
        window generator
        python & scala services
        reindexer use of VHS

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
    