# ebsco_adapter

## Architecture

Adapter for ingesting data from EBSCO. It fetches MARCXML records from the EBSCO FTP service, stores them in S3, and notifies the catalogue pipeline of updates.

```mermaid
C4Container
    title EBSCO Adapter Architecture

    System_Boundary(public_internet, "Public Internet") {
        System_Ext(ebsco_ftp, "EBSCO FTP", "E-resources provider, MARCXML in FTP")
    }

    System_Boundary(platform_account, "Platform AWS Account") {
        Container(ebsco_adapter, "EBSCO Adapter", "ECS Service", "Fetches data from the EBSCO FTP service.")
        ContainerDb(ebsco_s3, "EBSCO Source Records", "S3", "Stores EBSCO MARC records.")
        Container(catalogue_pipeline, "Catalogue Pipeline", "ECS Service(s)", "Updates to the catalogue pipeline.")
    }

    System_Boundary(elastic_Cloud, "Elastic Cloud AWS Account") {
        ContainerDb(catalogue_elastic, "Catalogue Pipeline Elasticsearch", "Elastic Cloud", "Stores data for the public catalogue.")
    }

    Rel(ebsco_adapter, ebsco_ftp, "Gets record updates", "HTTPS/API")
    Rel(ebsco_adapter, ebsco_s3, "Writes documents to", "S3")
    Rel(ebsco_s3, catalogue_pipeline, "Gets updated documents", "Notified by SNS/SQS")
    Rel(catalogue_pipeline, catalogue_elastic, "Records updated documents", "Notified by SNS/SQS")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="2")
```

## Repositories

See the following repositories for the code and configuration related to the EBSCO adapter:

- [wellcomecollection/catalogue-pipeline](https://github.com/wellcomecollection/catalogue-pipeline/tree/main/ebsco_adapter)

## Accounts

- [platform](../../aws_accounts.md#platform)