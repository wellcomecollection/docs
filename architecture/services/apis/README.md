# Wellcome Collection API Services

- [search_api](#search_api)
- [content_api](#content_api)
- [concepts_api](#concepts_api)
- [data_api](#data_api)
- [items_api](#items_api)
- [identity_api](#identity_api)
- [requesting_api](#requesting_api)
- [iiif.wellcomecollection.org](#iiifwellcomecollectionorg)

## search_api

The Catalogue search API is responsible for handling search requests across the Wellcome Collection's digital catalogue. It provides endpoints for searching images and works

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

See the following repositories for more details on the services described above:

- [wellcomecollection/catalogue-api](https://github.com/wellcomecollection/catalogue-api)

## concepts_api

The Concepts API is responsible for managing and retrieving information about concepts within the Wellcome Collection's digital catalogue. It provides endpoints for searching and browsing concepts.

```mermaid
C4Container
    title Container Diagram for the Concepts API

    System(client_app, "Client Application", "e.g., content_frontend, requesting concept data.")

    System_Boundary(platform_account, "Platform AWS Account") {
        Container(api_cloudfront, "CloudFront (api.wellcomecollection.org)", "AWS CDN", "Main entry point for all APIs.")
    }

    System_Boundary(catalogue_account, "Catalogue AWS Account") {
        Container(api_gateway, "API Gateway", "AWS API Gateway", "Custom domain: catalogue.api-prod.wellcomecollection.org")
        Container(nlb_catalogue, "Network Load Balancer", "AWS Catalogue NLB ", "Routes traffic to backend services.")
        Container(concepts_api, "Concepts API", "ECS Service", "Handles concept searches and retrieval.")
    }

    System_Boundary(elastic_Cloud, "Elastic Cloud AWS Account") {
        System_Ext(elastic_cloud_catalogue, "Catalogue Pipeline Cluster", "SaaS", "Hosts the catalogue-pipeline concept indexes.")
    }

    Rel(client_app, api_cloudfront, "Requests /catalogue/v2/...", "HTTPS")
    Rel(api_cloudfront, api_gateway, "Routes '/catalogue' path to")
    Rel(api_gateway, nlb_catalogue, "Routes requests to")
    Rel(nlb_catalogue, concepts_api, "Routes port 8000 for specific paths to")

    Rel(concepts_api, elastic_cloud_catalogue, "Queries index via", "AWS PrivateLink")

    UpdateLayoutConfig($c4ShapeInRow="1", $c4BoundaryInRow="3")
```

See the following repositories for more details on the services described above:

- [wellcomecollection/catalogue-api](https://github.com/wellcomecollection/catalogue-api)

## content_api

The Content API is responsible for managing and retrieving editorial content. It provides endpoints for searching content beyond what is available from Prismic APIs.

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

See the following repositories for more details on the services described above:

- [wellcomecollection/content-api](https://github.com/wellcomecollection/content-api)