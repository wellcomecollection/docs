# search_api

The Catalogue search API is responsible for handling search requests across the Wellcome Collection's digital catalogue. It provides endpoints for searching images and works

## Architecture

```mermaid
C4Container
    title Container Diagram for the Search API

    System(client_app, "Client Application", "e.g., content_frontend, requesting search results.")

    System_Boundary(platform_account, "Platform AWS Account") {
        Container(api_cloudfront, "CloudFront (api.wellcomecollection.org)", "AWS CDN", "Main entry point for all APIs.")
    }

    System_Boundary(catalogue_account, "Catalogue AWS Account") {
        Container(api_gateway, "API Gateway", "AWS API Gateway", "Custom domain: catalogue.api-prod.wellcomecollection.org")
        Container(nlb_catalogue, "Network Load Balancer", "AWS Catalogue NLB ", "Routes traffic to backend services.")
        Container(search_api, "Search API", "ECS Service", "Handles image and work searches.")
    }

    System_Boundary(elastic_Cloud, "Elastic Cloud AWS Account") {
        System_Ext(elastic_cloud_catalogue, "Catalogue Pipeline Cluster", "SaaS", "Hosts the catalogue-pipeline search indexes.")
    }

    Rel(client_app, api_cloudfront, "Requests /catalogue/v2/...", "HTTPS")
    Rel(api_cloudfront, api_gateway, "Routes '/catalogue' path to")
    Rel(api_gateway, nlb_catalogue, "Routes requests to")
    Rel(nlb_catalogue, search_api, "Routes port 8000 for specific paths to")

    Rel(search_api, elastic_cloud_catalogue, "Queries index via", "AWS PrivateLink")

    UpdateLayoutConfig($c4ShapeInRow="1", $c4BoundaryInRow="3")
```

## Accounts

- [catalogue](../../aws_accounts.md#catalogue)

## Repositories

See the following repositories for more details on the services described above:

- [wellcomecollection/catalogue-api](https://github.com/wellcomecollection/catalogue-api)
- [wellcomecollection/catalogue-pipeline](https://github.com/wellcomecollection/catalogue-pipeline)
