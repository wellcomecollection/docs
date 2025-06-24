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
- [wellcomecollection/catalogue-pipeline](https://github.com/wellcomecollection/catalogue-pipeline)

## concepts_api

The Concepts API is responsible for managing and retrieving information about concepts within the Wellcome Collection's digital catalogue. It provides endpoints for retrieving concept data.

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
- [wellcomecollection/catalogue-pipeline](https://github.com/wellcomecollection/catalogue-pipeline)

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

## data_api

The Data API provides endpoints for retrieving bulk data snapshots of the Wellcome Collection's digital catalogue. It allows users to download large datasets in gzipped JSONL format.

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

See the following repositories for more details on the services described above:

- [wellcomecollection/catalogue-api](https://github.com/wellcomecollection/catalogue-api)
- [wellcomecollection/developers.wellcomecollection.org](https://github.com/wellcomecollection/developers.wellcomecollection.org)
- [wellcomecollection/catalogue-pipeline](https://github.com/wellcomecollection/catalogue-pipeline)

## items_api

The Items API provides endpoints for retrieving information about individual items in the Wellcome Collection's digital catalogue. It gets the freshest data for items from Sierra directly.

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

See the following repositories for more details on the services described above:

- [wellcomecollection/catalogue-api](https://github.com/wellcomecollection/catalogue-api)
- [wellcomecollection/catalogue-pipeline](https://github.com/wellcomecollection/catalogue-pipeline)

## identity_api

The Identity API is responsible for managing user identity and authentication. It provides endpoints for user registration, and profile management.

```mermaid
C4Container
    title Container Diagram for the Identity API

    System(client_app, "Client Application", "e.g., identity_frontend, making user management requests.")

    System_Boundary(aws_identity, "Identity Account (AWS)") {
        Container(api_gateway, "API Gateway", "AWS API Gateway", "Custom domain: v1-api.account.wellcomecollection.org")
        Container(authorizer_lambda, "API Authorizer", "AWS Lambda", "Authorizes requests against Auth0.")
        Container(identity_api_lambda, "Identity API", "AWS Lambda", "Handles user management logic.")
    }

    System_Boundary(public_internet, "Public Internet") {
        System_Boundary(auth0_tenant, "Auth0 tenant") {
            System_Ext(auth0, "Auth0 APIs", "SaaS", "Manages user authentication and tokens.")
        }
        System_Ext(sierra, "Sierra", "3rd Party Cloud-Hosted Library Management System", "The system of record for library members.")
    }

    Rel(client_app, api_gateway, "Makes API request with token", "HTTPS")
    Rel(api_gateway, authorizer_lambda, "Uses authorizer to validate token")
    Rel(authorizer_lambda, identity_api_lambda, "Forwards authorized request to")
    Rel(identity_api_lambda, auth0, "Performs user management actions with")
    Rel(identity_api_lambda, sierra, "Performs user management actions with")

    UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="2")
```

See the following repositories for more details on the services described above:

- [wellcomecollection/identity](https://github.com/wellcomecollection/identity)