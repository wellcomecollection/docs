# ingest_inspector

## Architecture

A tool for inspecting data being ingested into the storage service.

The ingest inspector is a monitoring and debugging tool for the storage service. It is deployed entirely within the storage AWS account. The frontend is a static web application served from an S3 bucket behind a dedicated CloudFront distribution. The backend is an API Gateway endpoint backed by a Lambda function, which provides access to ingest and bag data for inspection by calling the storage service ingest API.

See https://github.com/wellcomecollection/storage-service/tree/main/monitoring/ingest_inspector for more details.

```mermaid
C4Container
    title Ingest Inspector Architecture

    System_Boundary(storage_account, "Storage AWS Account") {
        Container(frontend_s3, "Ingest Inspector Frontend", "S3 + CloudFront", "Static web app for inspecting ingests.")
        Container(api_gateway, "API Gateway", "AWS API Gateway", "Exposes backend API endpoints.")
        Container(lambda_backend, "Backend Lambda", "AWS Lambda", "Serves API requests for ingest/bag data.")
        Container_Ext(storage_ingest_api, "Storage Service Ingest API", "API Gateway", "Provides ingest and bag data.")
    }

    Rel(frontend_s3, api_gateway, "Fetches ingest/bag data from")
    Rel(api_gateway, lambda_backend, "Invokes Lambda for API requests")
    Rel(lambda_backend, storage_ingest_api, "Fetches ingest/bag data from")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

## Repositories

See the following repositories for the code and configuration related to the ingest inspector:

- [wellcomecollection/storage-service](https://github.com/wellcomecollection/storage-service/tree/main/monitoring/ingest_inspector)

## Accounts

- [storage](../../aws_accounts.md#storage)