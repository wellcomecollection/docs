# content_api

The Content API is responsible for managing and retrieving editorial content. It provides endpoints for searching content beyond what is available from Prismic APIs.

## Architecture

```mermaid
  C4Container
    title Container Diagram for the Content API

    System(client_app, "Client Application", "e.g., content_frontend, requesting concept data.")

    System_Boundary(platform_account, "Platform AWS Account") {
        Container(api_cloudfront, "CloudFront (api.wellcomecollection.org)", "AWS CDN", "Main entry point for all APIs.")
    }

    System_Boundary(catalogue_account, "Catalogue AWS Account") {
        Container(api_gateway, "API Gateway", "AWS API Gateway", "Custom domain: content.api-prod.wellcomecollection.org")
        Container(nlb_content, "Network Load Balancer", "AWS Content NLB ", "Routes traffic to backend services.")
        Container(content_api, "Content API", "ECS Service", "Handles content searches and retrieval.")
        Container(content_pipeline, "Content Pipeline", "AWS Lambda", "Indexes content for search.")

    }

    System_Boundary(third_party, "Third Party services") {

        System_Boundary(elastic_Cloud, "Elastic Cloud AWS Account") {
            System_Ext(elastic_cloud_content, "Content Pipeline Cluster", "SaaS", "Hosts the content pipeline indexes.")
        }

        System_Boundary(public_internet, "Public Internet") {
            System_Ext(prismic, "Prismic APIs", "External Headless CMS")
        }
    }

    Rel(client_app, api_cloudfront, "Requests /catalogue/v2/...", "HTTPS")
    Rel(api_cloudfront, api_gateway, "Routes '/catalogue' path to")
    Rel(api_gateway, nlb_content, "Routes requests to")
    Rel(nlb_content, content_api, "Routes port 8000 for specific paths to")
    Rel(content_pipeline, prismic, "Recieves content updates")
    Rel(content_pipeline, elastic_cloud_content, "Indexes content")
    Rel(content_api, elastic_cloud_content, "Queries index via", "AWS PrivateLink")

    UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="3")
```

## Accounts

- [catalogue](../../aws_accounts.md#catalogue)

## Repositories

See the following repositories for more details on the services described above:

- [wellcomecollection/content-api](https://github.com/wellcomecollection/content-api)
