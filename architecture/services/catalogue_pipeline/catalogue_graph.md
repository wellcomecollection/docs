# catalogue_graph

## Architecture

The catalogue graph pipeline is a serverless, event-driven system for building and maintaining a knowledge graph of concepts, names, and locations, enriched with data from external sources. It integrates with the existing catalogue pipeline to provide a comprehensive view of Wellcome Collection concepts and their relationships.

For a more detailed overview, see the Catalogue Graph Pipline RFC: https://github.com/wellcomecollection/docs/blob/main/rfcs/066-graph_pipeline/README.md

```mermaid
C4Container
    title Catalogue Graph Architecture

    System_Boundary(data_sources, "Data Sources") {
        System_Boundary(catalogue_pipeline, "Catalogue Pipeline") {
            System_Ext(catalogue_pipeline, "Catalogue Pipeline", "Provides Wellcome concepts and updates")
        }

        System_Boundary(external_sources, "External Sources") {
            System_Ext(lc, "Library of Congress (LCSH/LCNAF)", "Concepts, names, locations")
            System_Ext(mesh, "MeSH", "Medical Subject Headings")
            System_Ext(wikidata, "Wikidata", "Concepts, names, locations, links")
        }
    }

    System_Boundary(platform_account, "Platform AWS Account") {
        System_Boundary(graph_etl, "Graph Database ETL (Step Functions)") {
            Container(extractor, "extractor", "AWS Lambda", "Extracts, transforms, and batches concepts from sources.")
            ContainerDb(s3, "S3", "S3", "Stores bulk load files for Neptune.")
            Container(bulk_loader, "bulk_loader", "AWS Lambda", "Triggers Neptune bulk load from S3 (bulk mode).")
            ContainerDb(neptune, "AWS Neptune", "Graph DB", "Stores the catalogue knowledge graph.")
        }
        System_Boundary(elasticsearch_etl, "Elasticsearch ETL (Step Functions)") {
            Container(indexer, "indexer", "AWS Lambda", "Executes openCypher queries for incremental updates.")
        }
    }

    System_Boundary(elastic_Cloud, "Elastic Cloud AWS Account") {
        System_Ext(elastic_cloud_catalogue, "Catalogue Pipeline Cluster", "SaaS", "Hosts the catalogue-pipeline concept indexes.")
    }

    Rel(lc, extractor, "Provides LCSH/LCNAF data to", "HTTP/Download")
    Rel(mesh, extractor, "Provides MeSH data to", "HTTP/Download")
    Rel(wikidata, extractor, "Provides Wikidata data to", "HTTP/SPARQL")
    Rel(catalogue_pipeline, extractor, "Provides Wellcome concepts to", "SNS/S3")
    Rel(extractor, s3, "Writes extracted data to")
    Rel(s3, bulk_loader, "Loads bulk load data from")
    Rel(bulk_loader, neptune, "Loads edges and nodes to")
    Rel(neptune, indexer, "Indexes concept data to Elasticsearch")
    Rel(indexer, elastic_cloud_catalogue, "Indexes concept data to ES")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="5")
```

The pipeline loads and enriches concepts from the Wellcome catalogue and external ontologies (LCSH, LCNAF, MeSH, Wikidata), and writes the resulting graph to AWS Neptune. Bulk loads are triggered via S3 and the Neptune bulk loader; incremental updates are processed via SNS/SQS and Lambda. All orchestration is managed by AWS Step Functions.

See: https://github.com/wellcomecollection/catalogue-pipeline/tree/main/catalogue_graph

## Repositories

See the following repositories for more details on the services described above:

- [wellcomecollection/catalogue-pipeline](https://github.com/wellcomecollection/catalogue-pipeline/tree/main/catalogue_graph)

## Accounts

- [platform](../../aws_accounts.md#platform)