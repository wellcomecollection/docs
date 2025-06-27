# toggles.wellcomecollection.org

This service provides a JSON endpoint for feature flags and A/B testing toggles. It is used by the main website to determine which features are enabled for the user.

## Architecture

```mermaid
C4Container
    title Combined view of a user request and server-side toggle fetching

    Person(user, "Website User", "A visitor to wellcomecollection.org")

    System_Boundary(experience_account, "Experience AWS Account") {
        Container(main_cloudfront, "CloudFront (wellcomecollection.org)", "AWS CDN", "Main entry point for the website.")
        Container(alb, "Application Load Balancer", "AWS ALB", "Routes application traffic.")
        ContainerDb(toggles_s3, "S3 Bucket (toggles)", "AWS S3", "Hosts the static JSON file of toggles.")
    }

    Rel(user, main_cloudfront, "1. Requests a page", "HTTPS")
    Rel(main_cloudfront, alb, "2. Routes request to")
    Rel(alb, content_frontend, "3. Forwards request to")

    Rel(content_frontend, toggles_cloudfront, "4. Fetches toggles.json", "HTTPS (Server-Side)")
    Rel(toggles_cloudfront, toggles_s3, "5. Pulls file from")
```

## Accounts

- [experience](../../aws_accounts.md#experience)

## Repositories

See the following repositories for more details on the services described above:

- [wellcomecollection/wellcomecollection.org](https://github.com/wellcomecollection/wellcomecollection.org)
