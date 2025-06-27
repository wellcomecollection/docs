# storage_service

## Architecture

The storage service is responsible for the long-term preservation of our digital assets. It ensures that files are stored securely, their integrity is maintained, and they can be retrieved when needed.

The service is designed as a pipeline of applications that work together to process and store "bags" of files, which are packaged using the [BagIt specification](https://tools.ietf.org/html/rfc8493).

```mermaid
C4Container
    title Simplified Container diagram for Storage Service

    System_Boundary(platform_account, "Platform AWS Account") {
        Container(api_cloudfront, "CloudFront (api.wellcomecollection.org)", "AWS CDN", "Routes API requests.")
    }

    System_Boundary(storage_account, "Storage AWS Account") {
        Container(api_gateway, "API Gateway", "AWS API Gateway", "Exposes the Ingests and Bags APIs at storage.api.wellcomecollection.org")
        Container(storage_pipeline, "Storage Pipeline", "ECS Services", "A pipeline of Scala apps that verify and replicate bags.")
        
        ContainerDb(permanent_bucket, "Permanent Storage", "AWS S3", "Primary storage for bags (Standard-IA).")
    }

    System_Boundary(workflow_account, "Workflow AWS Account") {
        ContainerDb(ingests_bucket, "Ingests Bucket", "AWS S3", "Temporary storage for uploaded bags.")
    }
    
    Rel(api_cloudfront, api_gateway, "Forwards requests to")
    
    Rel(api_gateway, storage_pipeline, "Initiates ingest process")
    
    Rel(storage_pipeline, ingests_bucket, "Reads from")
    Rel(storage_pipeline, permanent_bucket, "Writes to")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="2")
```

For a more detailed breakdown of the architecture, see the [architecture documentation in the storage-service repository](https://github.com/wellcomecollection/storage-service/blob/main/docs/architecture.md).

## Repositories

- [wellcomecollection/storage-service](https://github.com/wellcomecollection/storage-service)

## Accounts

- [storage](../../aws_accounts.md#storage)
