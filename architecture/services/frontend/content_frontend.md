# content_frontend

This service is built with Next.js and provide the main website content and catalogue search functionality.

## Architecture

```mermaid
C4Container
    title Container Diagram for wellcomecollection.org with Account Boundaries

    Person(user, "Website User", "A visitor to wellcomecollection.org")

    System_Boundary(experience_account, "Experience AWS Account") {
        Container(cloudfront, "CloudFront", "AWS CDN", "Receives all user traffic and routes based on URL path.")
        ContainerDb(s3, "S3 Bucket", "AWS S3", "Serves static assets for the website.")
        Container(alb, "Application Load Balancer", "AWS ALB", "Routes application traffic to the correct frontend service.")

        Container(content_frontend, "Content Frontend", "ECS Service", "Renders the main website content.")
    }

    System_Boundary(catalogue_account, "Catalogue AWS Account") {
        Container(content_api, "Content API", "ECS Service")
        Container(catalogue_api, "Catalogue API", "ECS Service")
        Container(search_api, "Search API", "ECS Service")
        Container(concepts_api, "Concepts API", "ECS Service")
        Container(items_api, "Items API", "ECS Service")
    }

    System_Boundary(public_internet, "Public Internet") {
        System_Ext(prismic, "Prismic APIs", "External Headless CMS")
    }

    System_Boundary(digirati_account, "Digirati AWS Account") {
        Container(iiif_api, "IIIF Image API", "ECS Service", "iiif.wellcomecollection.org")
    }

    Rel(user, cloudfront, "Visits wellcomecollection.org", "HTTPS")

    Rel(cloudfront, s3, "Routes requests for static assets to")
    Rel(cloudfront, alb, "Routes all other requests to")

    Rel(alb, content_frontend, "Routes requests to", "Default traffic")

    Rel(content_frontend, prismic, "Requests data from")
    Rel(content_frontend, content_api, "Requests data from")
    Rel(content_frontend, catalogue_api, "Requests data from")
    Rel(content_frontend, search_api, "Requests data from")
    Rel(content_frontend, concepts_api, "Requests data from")
    Rel(content_frontend, items_api, "Requests data from")
    Rel(content_frontend, iiif_api, "Requests images from")
```

## Accounts

- [experience](../../aws_accounts.md#experience)

## Repositories

See the following repositories for more details on the services described above:

- [wellcomecollection/wellcomecollection.org](https://github.com/wellcomecollection/wellcomecollection.org)
- [wellcomecollection/catalogue-api](https://github.com/wellcomecollection/catalogue-api)
