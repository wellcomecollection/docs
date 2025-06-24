# items_api

The Items API provides endpoints for retrieving information about individual items in the Wellcome Collection's digital catalogue. It gets the freshest data for items from Sierra directly.

## Architecture

```mermaid
C4Container
    title Container Diagram for the Items API

    System(client_app, "Client Application", "e.g., content_frontend, requesting catalogue items.")

    System_Boundary(platform_account, "Platform AWS Account") {
        Container(api_cloudfront, "CloudFront (api.wellcomecollection.org)", "AWS CDN", "Main entry point for all APIs.")
    }

    System_Boundary(catalogue_account, "Catalogue AWS Account") {
        Container(api_gateway, "API Gateway", "AWS API Gateway", "Custom domain: catalogue.api-prod.wellcomecollection.org")
        Container(nlb_catalogue, "Network Load Balancer", "AWS Catalogue NLB ", "Routes traffic to backend services.")
        System_Boundary(ecs_services, "Catalogue ECS Cluster") {
            Container(items_api, "Items API", "ECS Service", "Handles catalogue items requests.")
            Container(search_api, "Search API", "ECS Service", "Handles requests for works and images.")
        }
    }

    System_Boundary(public_internet, "Public Internet") {
        System_Ext(sierra, "Sierra", "3rd Party Cloud-Hosted Library Management System", "The system of record for library members.")
    }

    System_Boundary(elastic_Cloud, "Elastic Cloud AWS Account") {
        System_Ext(elastic_cloud_catalogue, "Catalogue Pipeline Cluster", "SaaS", "Hosts the catalogue-pipeline search indexes.")
    }

    Rel(client_app, api_cloudfront, "Requests /catalogue/v2/...", "HTTPS")
    Rel(api_cloudfront, api_gateway, "Routes '/catalogue' path to")
    Rel(api_gateway, nlb_catalogue, "Routes requests to")
    Rel(nlb_catalogue, items_api, "Routes ports for specific paths to")

    Rel(items_api, search_api, "Get latest version of work data")
    Rel(search_api, elastic_cloud_catalogue, "Queries index via", "AWS PrivateLink")
    Rel(items_api, sierra, "Queries Sierra API to update item records")

    UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="2")
```

## Accounts

- [catalogue](../../aws_accounts.md#catalogue)

## Repositories

See the following repositories for more details on the services described above:

- [wellcomecollection/catalogue-api](https://github.com/wellcomecollection/catalogue-api)
- [wellcomecollection/catalogue-pipeline](https://github.com/wellcomecollection/catalogue-pipeline)
