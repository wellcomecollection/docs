# mets_adapter

## Architecture

Adapter for ingesting METS XML data. METS (Metadata Encoding and Transmission Standard) is a standard for encoding descriptive, administrative, and structural metadata for digital objects. It is the output of digital preservation workflow systems like Archivematica & Goobi, and is used to represent complex digital objects with multiple files and metadata.

This service refers to data stored in the [Wellcome Storage Service](../workflow/storage_service.md), and is used to ingest data into the main catalogue.

```mermaid
C4Container
    title METS Adapter Architecture

    System_Boundary(storage_account, "Storage AWS Account") {
        Container(storage_service, "Wellcome Storage Service", "ECS Service(s)")
    }

    System_Boundary(platform_account, "Platform AWS Account") {
        Container(mets_adapter, "METS Adapter", "ECS Service", "Fetches data from the Storage service and writes to the METS VHS.")
        ContainerDb(mets_vhs, "METS VHS", "DynamoDB/S3", "Stores METS data.")
        Container(catalogue_pipeline, "Catalogue Pipeline", "ECS Service(s)", "Updates to the catalogue pipeline.")
    }

    System_Boundary(elastic_Cloud, "Elastic Cloud AWS Account") {
        ContainerDb(catalogue_elastic, "Catalogue Pipeline Elasticsearch", "Elastic Cloud", "Stores data for the public catalogue.")
    }

    Rel(mets_adapter, storage_service, "Gets record updates", "HTTPS/API")
    Rel(mets_adapter, mets_vhs, "Writes documents to", "DynamoDB/S3")
    Rel(mets_vhs, catalogue_pipeline, "Gets updated documents", "Notified by SNS/SQS")
    Rel(catalogue_pipeline, catalogue_elastic, "Records updated documents", "Notified by SNS/SQS")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="2")
```

## Repositories

See the following repositories for the code and configuration related to the METS adapter:

- [wellcomecollection/catalogue-pipeline](https://github.com/wellcomecollection/catalogue-pipeline/tree/main/mets_adapter)

## Accounts

- [platform](../../aws_accounts.md#platform)
