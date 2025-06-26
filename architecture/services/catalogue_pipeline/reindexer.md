# reindexer

## Architecture

The service for re-indexing catalogue data, it sends data from the catalogue pipeline adapter source data stores through the catalogue pipeline to be re-transformed and re-indexed in the catalogue pipeline Elasticsearch index.

Adapters should expose source data in a way that allows the reindexer uses to trigger re-indexing of data. 

SeeL https://github.com/wellcomecollection/catalogue-pipeline/tree/main/reindexer for more details on the reindexer service architecture.

```mermaid
C4Container
    title Catalogue Graph Architecture

    System_Boundary(platform_account, "Platform AWS Account") {
        Container(reindex_worker, "Reindex Worker", "ECS Service", "Fetches data source adapter.")
        ContainerDb(source_vhs, "Source VHS (Versioned Hybrid Store)", "DynamoDB/S3", "Stores source data in VHS format.")
        Container(transformer, "Transformer", "ECS Service(s)", "Transforms data for the catalogue pipeline.")
    }

    Rel(reindex_worker, source_vhs, "Reads records to be reindexed", "HTTP/Download")
    Rel(reindex_worker, transformer, "Informs transformer of records to be reindexed", "HTTP/Download")
    Rel(transformer, source_vhs,  "Retrieves and transforms source data", "HTTP/Download")

    UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="5")
```

## Repositories

See the following repositories for more details on the services described above:

- [wellcomecollection/catalogue-pipeline](https://github.com/wellcomecollection/catalogue-pipeline/tree/main/reindexer)

## Accounts

- [platform](../../aws_accounts.md#platform)
