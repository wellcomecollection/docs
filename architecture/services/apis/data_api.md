# data_api

The Data API provides endpoints for retrieving bulk data snapshots of the Wellcome Collection's digital catalogue. It allows users to download large datasets in gzipped JSONL format.

## Architecture

```mermaid
C4Container
    title Container Diagram for the Data API (data.wellcomecollection.org)

    Person(developer, "Developer", "A researcher or developer wanting to use the bulk data.")
    System_Ext(github_pages, "Developer Portal (GitHub Pages)", "developers.wellcomecollection.org")

    System_Boundary(c1, "Catalogue AWS Account") {
        Container(data_cloudfront, "CloudFront (data.wellcomecollection.org)", "AWS CDN", "Serves gzipped JSONL data files.")
        ContainerDb(data_s3, "S3 Bucket", "AWS S3", "Stores the bulk data snapshots.")
        Container(snapshot_lambda, "Snapshot Lambda", "AWS Lambda", "Generates and uploads gzipped JSONL snapshots.")
    }

    System_Boundary(elastic_Cloud, "Elastic Cloud AWS Account") {
        System_Ext(elastic_cloud_catalogue, "Catalogue Pipeline Cluster", "SaaS", "Hosts the catalogue-pipeline concept indexes.")
    }

    Rel(developer, github_pages, "1. Reads documentation")
    Rel(github_pages, data_cloudfront, "2. Links to data files on")
    Rel(developer, data_cloudfront, "3. Downloads data file from", "HTTPS")
    Rel(data_cloudfront, data_s3, "4. Serves file from")

    Rel(snapshot_lambda, data_s3, "Uploads gzipped JSONL files to")
    Rel(snapshot_lambda, elastic_cloud_catalogue, "Retrieves snapshot data")
```

## Accounts

- [catalogue](../../aws_accounts.md#catalogue)

## Repositories

See the following repositories for more details on the services described above:

- [wellcomecollection/catalogue-api](https://github.com/wellcomecollection/catalogue-api)
- [wellcomecollection/developers.wellcomecollection.org](https://github.com/wellcomecollection/developers.wellcomecollection.org)
- [wellcomecollection/catalogue-pipeline](https://github.com/wellcomecollection/catalogue-pipeline)
