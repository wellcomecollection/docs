# identity_frontend

This service is built with Next.js and provides some user account management features.

## Architecture

```mermaid
C4Container
    title Container Diagram for identity_frontend on wellcomecollection.org

    Person(user, "Website User", "A visitor to wellcomecollection.org")

    System_Boundary(experience_account, "Experience AWS Account") {
        Container(cloudfront, "CloudFront", "AWS CDN", "Receives all user traffic and routes based on URL path.")
        Container(alb, "Application Load Balancer", "AWS ALB", "Routes application traffic to the correct frontend service.")
        Container(identity_frontend, "Identity Frontend", "ECS Service", "Renders the '/account' pages.")
    }

    System_Boundary(identity_account, "Identity AWS Account") {
        Container(requesting_api, "Requesting API", "ECS Service")
        Container(identity_api, "Identity API", "AWS Lambda", "v1-api.account.wellcomecollection.org")
    }

    Rel(user, cloudfront, "Visits wellcomecollection.org", "HTTPS")
    Rel(cloudfront, alb, "Routes all other requests to")
    Rel(alb, identity_frontend, "Routes '/account/*' requests to")
    Rel(identity_frontend, identity_api, "Requests data from")
    Rel(identity_frontend, requesting_api, "Requests data from")

    UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="2")
```

## Accounts

- [experience](../../aws_accounts.md#experience)

## Repositories

- [wellcomecollection/wellcomecollection.org](https://github.com/wellcomecollection/wellcomecollection.org)
- [wellcomecollection/catalogue-api](https://github.com/wellcomecollection/catalogue-api)
- [wellcomecollection/identity](https://github.com/wellcomecollection/identity)
