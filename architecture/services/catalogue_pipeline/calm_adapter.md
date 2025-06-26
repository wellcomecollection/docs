# calm_adapter

## Architecture

Adapter for ingesting data from the Calm archive management system.

```mermaid
C4Container
    title Calm Adapter Architecture

    System_Boundary(public_internet, "Public Internet") {
        System_Ext(calm, "Calm", "Archive management system")
    }

    System_Boundary(platform_account, "Platform AWS Account") {
        Container(calm_adapter, "calm_adapter", "ECS Service", "Fetches data from Calm and writes to the Calm VHS.")
        ContainerDb(calm_vhs, "Calm VHS", "DynamoDB/S3", "Stores Calm data.")
        Container(calm_indexer, "calm_indexer", "AWS Lambda", "Indexes Calm data into the reporting Elasticsearch cluster.")
        Container(catalogue_pipeline, "Catalogue Pipeline", "ECS Service(s)", "Updates to the catalogue pipeline.")
    }

    System_Boundary(elastic_Cloud, "Elastic Cloud AWS Account") {
        ContainerDb(catalogue_elastic, "Catalogue Pipeline Elasticsearch", "Elastic Cloud", "Stores data for the public catalogue.")
        ContainerDb(reporting_elastic, "Reporting Elasticsearch", "Elastic Cloud", "Stores indexed Calm data for reporting.")
    }

    Rel(calm_adapter, calm, "Gets record updates", "HTTPS/API")
    Rel(calm_adapter, calm_vhs, "Writes documents to", "DynamoDB/S3")
    Rel(calm_vhs, catalogue_pipeline, "Gets updated documents", "Notified by SNS/SQS")
    Rel(calm_vhs, calm_indexer, "Records updated documents", "Notified by SNS/SQS")
    Rel(catalogue_pipeline, catalogue_elastic, "Records updated documents", "Notified by SNS/SQS")
    Rel(calm_indexer, reporting_elastic, "Records updated documents", "Notified by SNS/SQS")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="2")
```

## Repositories

See the following repositories for more details on the services described above:

- https://github.com/wellcomecollection/catalogue-pipeline/tree/main/calm_adapter

## Accounts

- [platform](../../aws_accounts.md#platform)