# tei_adapter

## Architecture

Adapter for ingesting TEI XML data.

```mermaid
C4Container
    title TEI Adapter Architecture

    System_Boundary(public_internet, "Public Internet") {
        System_Ext(tei, "GitHub Repository", "TEI XML data repository")
    }

    System_Boundary(platform_account, "Platform AWS Account") {
        Container(tei_adapter, "tei_adapter", "ECS Service", "Fetches data from TEI and writes to the catalogue pipeline's Elasticsearch cluster.")
        ContainerDb(tei_vhs, "TEI Adapter Store", "DynamoDB", "Stores TEI data.")
        Container(tei_indexer, "tei_indexer", "AWS Lambda", "Indexes TEI data into the reporting Elasticsearch cluster.")
        Container(catalogue_pipeline, "Catalogue Pipeline", "ECS Service(s)", "Updates to the catalogue pipeline.")
    }

    System_Boundary(elastic_Cloud, "Elastic Cloud AWS Account") {
        ContainerDb(catalogue_elastic, "Catalogue Pipeline Elasticsearch", "Elastic Cloud", "Stores data for the public catalogue.")
        ContainerDb(reporting_elastic, "Reporting Elasticsearch", "Elastic Cloud", "Stores indexed TEI data for reporting.")
    }

    Rel(tei_adapter, tei, "Gets record updates", "HTTPS/API")
    Rel(tei_adapter, tei_vhs, "Writes documents to", "DynamoDB")
    Rel(tei_vhs, catalogue_pipeline, "Gets updated documents", "Notified by SNS/SQS")
    Rel(tei_vhs, tei_indexer, "Records updated documents", "Notified by SNS/SQS")
    Rel(catalogue_pipeline, catalogue_elastic, "Records updated documents", "Notified by SNS/SQS")
    Rel(tei_indexer, reporting_elastic, "Records updated documents", "Notified by SNS/SQS")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="2")
```

## Repositories

See the following repositories for more details on the services described above:

- [wellcomecollection/catalogue-pipeline](https://github.com/wellcomecollection/catalogue-pipeline/tree/main/tei_adapter)
- [wellcomecollection/wellcome-collection-tei](https://github.com/wellcomecollection/wellcome-collection-tei)

## Accounts

- [platform](../../aws_accounts.md#platform)