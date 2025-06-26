# sierra_adapter

## Architecture

Adapter for ingesting data from the Sierra library management system.

```mermaid
C4Container
    title Sierra Adapter Architecture

    System_Boundary(public_internet, "Public Internet") {
        System_Ext(sierra, "Sierra", "Library management system")
    }

    System_Boundary(platform_account, "Platform AWS Account") {
        Container(sierra_adapter, "sierra_adapter", "ECS Service", "Fetches data from Sierra and writes to the Sierra VHS.")
        ContainerDb(sierra_vhs, "Sierra VHS", "DynamoDB/S3", "Stores Sierra data.")
        Container(sierra_indexer, "sierra_indexer", "AWS Lambda", "Indexes Sierra data into the reporting Elasticsearch cluster.")
        Container(catalogue_pipeline, "Catalogue Pipeline", "ECS Service(s)", "Updates to the catalogue pipeline.")
    }

    System_Boundary(elastic_Cloud, "Elastic Cloud AWS Account") {
        ContainerDb(catalogue_elastic, "Catalogue Pipeline Elasticsearch", "Elastic Cloud", "Stores data for the public catalogue.")
        ContainerDb(reporting_elastic, "Reporting Elasticsearch", "Elastic Cloud", "Stores indexed Sierra data for reporting.")
    }

    Rel(sierra_adapter, sierra, "Gets record updates", "HTTPS/API")
    Rel(sierra_adapter, sierra_vhs, "Writes documents to", "DynamoDB/S3")
    Rel(sierra_vhs, catalogue_pipeline, "Gets updated documents", "Notified by SNS/SQS")
    Rel(sierra_vhs, sierra_indexer, "Records updated documents", "Notified by SNS/SQS")
    Rel(catalogue_pipeline, catalogue_elastic, "Records updated documents", "Notified by SNS/SQS")
    Rel(sierra_indexer, reporting_elastic, "Records updated documents", "Notified by SNS/SQS")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="2")

```

## Repositories

See the following repositories for more details on the services described above:

- https://github.com/wellcomecollection/catalogue-pipeline/tree/main/sierra_adapter

## Accounts

- [platform](../../aws_accounts.md#platform)