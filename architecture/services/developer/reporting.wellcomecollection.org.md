# reporting.wellcomecollection.org

## Architecture

Internal reporting dashboards and services, it provides:

- Dashboards to search source data from Calm, Sierra, and other sources. 
- Visibility on storage service ingests and files.

```mermaid
C4Container
    title Reporting Architecture

    System_Boundary(data_sources, "Data Sources") {
        System_Ext(catalogue_pipeline, "Catalogue Pipeline", "Provides source data from Calm, Sierra, etc.")
        System_Ext(storage_service, "Storage Service", "Provides ingest and file data.")
    }

    System_Boundary(elastic_cloud, "Elastic Cloud AWS Account") {
        ContainerDb(elasticsearch, "Elasticsearch", "Elastic Cloud", "Stores indexed reporting data.")
        Container(kibana, "Kibana", "Elastic Cloud", "Dashboards and visualisation.")
    }

    Rel(catalogue_pipeline, elasticsearch, "Sends source data to")
    Rel(storage_service, elasticsearch, "Sends ingest/file data to")
    Rel(elasticsearch, kibana, "Visualised in")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

## Repositories

See the following repositories for more details on the services described above:

- [wellcomecollection/platform-infrastructure](https://github.com/wellcomecollection/platform-infrastructure/tree/main/cloudfront/reporting.wellcomecollection.org)

## Accounts

- [platform](../../aws_accounts.md#platform)
- [storage](../../aws_accounts.md#storage)